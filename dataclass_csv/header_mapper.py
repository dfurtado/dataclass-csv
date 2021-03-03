from typing import Any, Callable


class HeaderMapper:
    """The `HeaderMapper` class is used to explicitly map property in a
    dataclass to a header. Useful when the header on the CSV file needs to
    be different from a dataclass property name.
    """

    def __init__(self, callback: Callable[[str], None]):
        def to(header: str) -> None:
            """Specify how a property in the dataclass will be
            displayed in the CSV file
            :param header: Specify the CSV title for the dataclass property
            """

            callback(header)

        self.to: Callable[[str], None] = to
