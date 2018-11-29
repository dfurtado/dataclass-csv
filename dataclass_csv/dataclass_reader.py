import dataclasses

from datetime import datetime
from csv import DictReader

from .field_mapper import FieldMapper
from .exceptions import MissingDecoratorError


class DataclassReader:
    def __init__(
        self,
        f,
        cls,
        fieldnames=None,
        restkey=None,
        restval=None,
        dialect='excel',
        *args,
        **kwds
    ):

        if not f:
            raise ValueError('The f argument is required')

        if cls is None or not dataclasses.is_dataclass(cls):
            raise ValueError('cls argument needs to be a dataclass')

        self.cls = cls
        self.optional_fields = self._get_optional_fields()
        self.field_mapping = {}

        self.reader = DictReader(
            f, fieldnames, restkey, restval, dialect, *args, **kwds
        )

    def _get_optional_fields(self):
        return [
            field.name
            for field in dataclasses.fields(self.cls)
            if not isinstance(field.default, dataclasses._MISSING_TYPE)
        ]

    def _add_to_mapping(self, property_name, csv_fieldname):
        self.field_mapping[property_name] = csv_fieldname

    def _get_value(self, row, field):
        try:
            key = (
                field.name
                if field.name not in self.field_mapping.keys()
                else self.field_mapping.get(field.name)
            )
            value = row[key]
        except KeyError:
            if field.name in self.optional_fields:
                return field.default
            else:
                raise KeyError(
                    f'The value {field.name} is missing in the CSV file.'
                )
        else:
            if not value and field.name in self.optional_fields:
                return field.default
            elif not value and field.name not in self.optional_fields:
                raise ValueError(
                    (
                        f'The field {field.name} is required. Verify if any '
                        'row in the CSV file is missing this data.'
                    )
                )
            else:
                return value

    def parse_date_value(self, field, date_value):
        if not hasattr(self.cls, '__date_format__'):
            raise MissingDecoratorError(
                (
                    'It was not possible to parse the value of the property '
                    f'`{field.name}` of type {field.type}. Make sure to use '
                    'the `@dateformat` decorator specifying the date format.'
                )
            )

        return datetime.strptime(date_value, self.cls.__date_format__)

    def _process_row(self, row):

        values = []

        for field in dataclasses.fields(self.cls):
            value = self._get_value(row, field)

            if (not value and field.default is None):
                values.append(None)
                continue

            if field.type is datetime:
                try:
                    transformed_value = self.parse_date_value(field, value)
                except ValueError:
                    raise
                else:
                    values.append(transformed_value)
                    continue

            try:
                transformed_value = field.type(value)
            except ValueError:
                raise ValueError(
                    (
                        f'The field {field.name} is defined as {field.type} '
                        f'but received a value of type {type(value)}.'
                    )
                )
            else:
                values.append(transformed_value)

        return self.cls(*values)

    def __next__(self):
        row = next(self.reader)
        return self._process_row(row)

    def __iter__(self):
        return self

    def map(self, csv_fieldname):
        return FieldMapper(
            lambda property_name: self._add_to_mapping(
                property_name, csv_fieldname
            )
        )
