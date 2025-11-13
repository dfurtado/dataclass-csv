import csv
import dataclasses
from typing import Type, Dict, Any, Iterable
from .header_mapper import HeaderMapper


class DataclassWriter:
    def __init__(
        self,
        f: Any,
        data: Iterable,
        cls: Type[object],
        dialect: str = "excel",
        **fmtparams: Dict[str, Any],
    ):
        if not f:
            raise ValueError("The f argument is required")

        try:
            iter(data)
        except TypeError:
            raise ValueError("Invalid 'data' argument. It must be an iterable")

        if not dataclasses.is_dataclass(cls):
            raise ValueError("Invalid 'cls' argument. It must be a dataclass")

        self._data = data
        self._cls = cls
        self._field_mapping: Dict[str, str] = dict()

        self._fieldnames = [x.name for x in dataclasses.fields(cls)]

        self._writer = csv.writer(f, dialect=dialect, **fmtparams)

    def _add_to_mapping(self, header: str, propname: str):
        self._field_mapping[propname] = header

    def _apply_mapping(self):
        mapped_fields = []

        for field in self._fieldnames:
            mapped_item = self._field_mapping.get(field, field)
            mapped_fields.append(mapped_item)

        return mapped_fields

    def write(self, skip_header: bool = False):
        if not skip_header:
            if self._field_mapping:
                self._fieldnames = self._apply_mapping()

            self._writer.writerow(self._fieldnames)

        for item in self._data:
            if not isinstance(item, self._cls):
                raise TypeError(
                    (
                        f"The item [{item}] is not an instance of "
                        f"{self._cls.__name__}. All items in the iterable must be "
                        "instances of the same type"
                    )
                )
            row = dataclasses.astuple(item)
            self._writer.writerow(row)

    def map(self, propname: str) -> HeaderMapper:
        """Used to map a field in the dataclass to header item in the CSV file
        :param propname: The name of the property of the dataclass to be mapped
        """
        return HeaderMapper(lambda header: self._add_to_mapping(header, propname))
