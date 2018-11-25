class FieldMapper:
    def __init__(self, callback):
        def to(property_name):
            callback(property_name)

        self.to = to
