from .header_mapper import HeaderMapper as HeaderMapper
from typing import Any, Dict, List, Type

class DataclassWriter:
    def __init__(
        self,
        f: Any,
        data: List[Any],
        cls: Type[object],
        dialect: str = ...,
        **fmtparams: Any,
    ) -> None: ...
    def write(self, skip_header: bool = ...) -> Any: ...
    def map(self, propname: str) -> HeaderMapper: ...
