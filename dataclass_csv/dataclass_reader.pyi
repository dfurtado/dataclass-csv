from .exceptions import CsvValueError as CsvValueError
from .field_mapper import FieldMapper as FieldMapper
from typing import Any, Dict, List, Optional, Sequence, Type

class DataclassReader:
    def __init__(
        self,
        f: Any,
        cls: Type[object],
        fieldnames: Optional[Sequence[str]] = ...,
        restkey: Optional[str] = ...,
        restval: Optional[Any] = ...,
        dialect: str = ...,
        *args: List[Any],
        **kwds: Dict[str, Any],
    ) -> None: ...
    def __next__(self): ...
    def __iter__(self) -> Any: ...
    def map(self, csv_fieldname: str) -> FieldMapper: ...
