import csv
import dataclasses
from typing import Type, Dict, Any, List, Iterable
from .header_mapper import HeaderMapper


class DataclassWriter:
    def __init__(
        self,
        f: Iterable[str],
        data: List[Any],
        cls: Type[object],
        dialect: str = "excel",
        **fmtparams: Dict[str, Any],
    ):
        if not f:
            raise ValueError("The f argument is required")

        if not isinstance(data, list):
            raise ValueError("Invalid 'data' argument. It must be a list")

        if not dataclasses.is_dataclass(cls):
            raise ValueError("Invalid 'cls' argument. It must be a dataclass")

        self.data = data
        self.cls = cls
        self.field_mapping = dict()

        self.fieldnames = [x.name for x in dataclasses.fields(cls)]

        self.writer = csv.writer(f, dialect=dialect, **fmtparams)

    def _add_to_mapping(self, header, propname):
        self.field_mapping[propname] = header

    def apply_mapping(self):
        mapped_fields = []

        for field in self.fieldnames:
            mapped_item = self.field_mapping.get(field, field)
            mapped_fields.append(mapped_item)

        return mapped_fields

    def write(self, skip_header: bool = False):
        if not skip_header:
            if self.field_mapping:
                self.fieldnames = self.apply_mapping()

            self.writer.writerow(self.fieldnames)

        for item in self.data:
            if not isinstance(item, self.cls):
                raise TypeError(
                    (
                        f"The item [{item}] is not an instance of {self.cls.__name__}. "
                        "All items on the list must be instances of the same type"
                    )
                )
            row = dataclasses.astuple(item)
            self.writer.writerow(row)

    def map(self, propname: str) -> HeaderMapper:
        """Used to map a field in the dataclass to header item in the CSV file
        :param propname: The name of the property of the dataclass to be mapped
        """
        return HeaderMapper(
            lambda header: self._add_to_mapping(header, propname)
        )
