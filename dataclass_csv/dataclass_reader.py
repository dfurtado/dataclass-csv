import dataclasses
import csv

from datetime import date, datetime
from typing import Union, Type, Optional, Sequence, Dict, Any

import typing

from .field_mapper import FieldMapper
from .exceptions import CsvValueError

from collections import Counter

def strtobool(value: str) -> bool:
    trueValues = ["true", "yes", "t", "y", "on", "1"]

    validValues =  ["false", "no", "f", "n", "off", "0", *trueValues]

    if value.lower() not in validValues:
        raise ValueError(f"invalid boolean value {value}")

    return value.lower() in trueValues


def _verify_duplicate_header_items(header):
    if header is not None and len(header) == 0:
        return

    header_counter = Counter(header)
    duplicated = [k for k, v in header_counter.items() if v > 1]

    if len(duplicated) > 0:
        raise ValueError(
            (
                "It seems like the CSV file contain duplicated header "
                f"values: {duplicated}. This may cause inconsistent data. "
                "Use the kwarg validate_header=False when initializing the "
                "DataclassReader to skip the header validation."
            )
        )


def is_union_type(t):
    if hasattr(t, "__origin__") and t.__origin__ is Union:
        return True

    return False


def get_args(t):
    if hasattr(t, "__args__"):
        return t.__args__

    return tuple()


class DataclassReader:
    def __init__(
        self,
        f: Any,
        cls: Type[object],
        fieldnames: Optional[Sequence[str]] = None,
        restkey: Optional[str] = None,
        restval: Optional[Any] = None,
        dialect: str = "excel",
        *args: Any,
        **kwds: Any,
    ):

        if not f:
            raise ValueError("The f argument is required.")

        if cls is None or not dataclasses.is_dataclass(cls):
            raise ValueError("cls argument needs to be a dataclass.")

        self._cls = cls
        self._optional_fields = self._get_optional_fields()
        self._field_mapping: Dict[str, Dict[str, Any]] = {}

        validate_header = kwds.pop("validate_header", True)

        self._reader = csv.DictReader(
            f, fieldnames, restkey, restval, dialect, *args, **kwds
        )

        if validate_header:
            _verify_duplicate_header_items(self._reader.fieldnames)

        self.type_hints = typing.get_type_hints(cls)

    def _get_optional_fields(self):
        return [
            field.name
            for field in dataclasses.fields(self._cls)
            if not isinstance(field.default, dataclasses._MISSING_TYPE)
            or not isinstance(field.default_factory, dataclasses._MISSING_TYPE)
        ]

    def _add_to_mapping(self, property_name, csv_fieldname):
        self._field_mapping[property_name] = csv_fieldname

    def _get_metadata_option(self, field, key):
        option = field.metadata.get(key, getattr(self._cls, f"__{key}__", None))
        return option

    def _get_default_value(self, field):
        return (
            field.default
            if not isinstance(field.default, dataclasses._MISSING_TYPE)
            else field.default_factory()
        )

    def _get_possible_keys(self, fieldname, row):
        possible_keys = list(filter(lambda x: x.strip() == fieldname, row.keys()))
        if possible_keys:
            return possible_keys[0]

    def _get_value(self, row, field):
        is_field_mapped = False

        try:
            if field.name in self._field_mapping.keys():
                is_field_mapped = True
                key = self._field_mapping.get(field.name)
            else:
                key = field.name

            if key in row.keys():
                value = row[key]
            else:
                possible_key = self._get_possible_keys(field.name, row)
                key = possible_key if possible_key else key
                value = row[key]

        except KeyError:
            if field.name in self._optional_fields:
                return self._get_default_value(field)
            else:
                keyerror_message = f"The value for the column `{field.name}`"
                if is_field_mapped:
                    keyerror_message = f"The value for the mapped column `{key}`"
                raise KeyError(f"{keyerror_message} is missing in the CSV file")
        else:
            if not value and field.name in self._optional_fields:
                return self._get_default_value(field)
            elif not value and field.name not in self._optional_fields:
                raise ValueError(f"The field `{field.name}` is required.")
            elif (
                value
                and field.type is str
                and not len(value.strip())
                and not self._get_metadata_option(field, "accept_whitespaces")
            ):
                raise ValueError(
                    (
                        f"It seems like the value of `{field.name}` contains "
                        "only white spaces. To allow white spaces to all "
                        "string fields, use the @accept_whitespaces "
                        "decorator. "
                        "To allow white spaces specifically for the field "
                        f"`{field.name}` change its definition to: "
                        f"`{field.name}: str = field(metadata="
                        "{'accept_whitespaces': True})`."
                    )
                )
            else:
                return value

    def _parse_date_value(self, field, date_value, field_type):
        dateformat = self._get_metadata_option(field, "dateformat")

        if not isinstance(date_value, str):
            return date_value

        if not dateformat:
            raise AttributeError(
                (
                    "Unable to parse the datetime string value. Date format "
                    "not specified. To specify a date format for all "
                    "datetime fields in the class, use the @dateformat "
                    "decorator. To define a date format specifically for this "
                    "field, change its definition to: "
                    f"`{field.name}: datetime = field(metadata="
                    "{'dateformat': <date_format>})`."
                )
            )

        datetime_obj = datetime.strptime(date_value, dateformat)

        if field_type == date:
            return datetime_obj.date()
        else:
            return datetime_obj

    def _process_row(self, row):
        values = dict()

        for field in dataclasses.fields(self._cls):
            if not field.init:
                continue

            try:
                value = self._get_value(row, field)
            except ValueError as ex:
                raise CsvValueError(ex, line_number=self._reader.line_num) from None

            if not value and field.default is None:
                values[field.name] = None
                continue

            field_type = self.type_hints[field.name]

            if is_union_type(field_type):
                type_args = [x for x in get_args(field_type) if x is not type(None)]
                if len(type_args) == 1:
                    field_type = type_args[0]

            if field_type is datetime or field_type is date:
                try:
                    transformed_value = self._parse_date_value(field, value, field_type)
                except ValueError as ex:
                    raise CsvValueError(ex, line_number=self._reader.line_num) from None
                else:
                    values[field.name] = transformed_value
                    continue

            if field_type is bool:
                try:
                    transformed_value = (
                        value
                        if isinstance(value, bool)
                        else strtobool(str(value).strip()) == 1
                    )
                except ValueError as ex:
                    raise CsvValueError(ex, line_number=self._reader.line_num) from None
                else:
                    values[field.name] = transformed_value
                    continue

            try:
                transformed_value = field_type(value)
            except ValueError as e:
                raise CsvValueError(
                    (
                        f"The field `{field.name}` is defined as {field.type} "
                        f"but received a value of type {type(value)}."
                    ),
                    line_number=self._reader.line_num,
                ) from e
            else:
                values[field.name] = transformed_value
        return self._cls(**values)

    def __next__(self):
        row = next(self._reader)
        return self._process_row(row)

    def __iter__(self):
        return self

    def map(self, csv_fieldname: str) -> FieldMapper:
        """Used to map a field in the CSV file to a `dataclass` field
        :param csv_fieldname: The name of the CSV field
        """
        return FieldMapper(
            lambda property_name: self._add_to_mapping(property_name, csv_fieldname)
        )
