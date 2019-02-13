class FieldMapper:
    """The `FieldMapper` class is used to explicitly map a field
    in the CSV file to a specific `dataclass` field.
    """

    def __init__(self, callback):
        def to(property_name):
            """Specify the dataclass field to receive the value
            :param property_name: The dataclass property that
            will receive the csv value.
            """

            callback(property_name)

        self.to = to
