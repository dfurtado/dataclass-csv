class CsvValueError(Exception):
    """Error when a value in the CSV file cannot be parsed."""

    def __init__(self, error, line_number):
        self.error = error
        self.line_number = line_number

    def __str__(self):
        return f'{self.error} [CSV Line number: {self.line_number}]'
