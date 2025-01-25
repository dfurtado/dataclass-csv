from typing import Any


class CsvValueError(Exception):
    """Error when a value in the CSV file cannot be parsed."""

    def __init__(self, error: Any, line_number: int):
        self.error: Any = error
        self.line_number: int = line_number

    def __str__(self):
        return f"{self.error} [CSV Line number: {self.line_number}]"
