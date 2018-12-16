def dateformat(date_format):
    if not date_format or not isinstance(date_format, str):
        raise ValueError('Invalid value for the date_format argument')

    def func(cls):
        cls.__dateformat__ = date_format
        return cls

    return func


def accept_whitespaces(cls=None):
    def func(cls):
        cls.__accept_whitespaces__ = True
        return cls

    if cls:
        return func(cls)

    return func
