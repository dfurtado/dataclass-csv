class CsvValueError(Exception):

    def __init__(self, msg, line_number):
        self.msg = msg
        self.line_number = line_number

    def __str__(self):
        return f'Error: {self.msg} [CSV Line number: {self.line_number}]'
