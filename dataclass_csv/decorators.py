from typing import Any, Callable, TypeVar, Type

F = TypeVar("F", bound=Callable[..., Any])


def dateformat(date_format: str) -> Callable[[F], F]:
    """The dateformat decorator is used to specify the format
    the `DataclassReader` should use when parsing datetime strings.

    Usage:
        >>> from dataclasses import dataclass
        >>> from datetime import datetime
        >>> from dataclass_csv import dateformat

        >>> @dataclass
        >>> @dateformat('%Y-%m-%d')
        >>> class User:
        >>>     firstname: str
        >>>     lastname: str
        >>>     brithday: datetime
    """

    if not date_format or not isinstance(date_format, str):
        raise ValueError("Invalid value for the date_format argument")

    def func(klass):
        klass.__dateformat__ = date_format
        return klass

    return func

KLASS = TypeVar("KLASS", bound=Type[Any])

def accept_whitespaces(klass: KLASS) -> Callable[[KLASS], KLASS]:
    """The accept_whitespaces decorator tells the `DataclassReader`
    that `str` fields defined in the `dataclass` should accept
    values containing only white spaces.

    Usage:
        >>> from dataclasses import dataclass
        >>> from dataclass_csv import accept_whitespaces

        >>> @dataclass
        >>> @accept_whitespaces
        >>> class User:
        >>>     firstname: str
        >>>     lastname: str
        >>>     brithday: datetime
    """

    klass.__accept_whitespaces__ = True
    return klass
