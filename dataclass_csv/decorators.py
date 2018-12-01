def dateformat(date_format):

    if not date_format or not isinstance(date_format, str):
        raise ValueError('Invalid value for the date_format argument')

    def func(cls):
        cls.__dateformat__ = date_format
        return cls

    return func


def accept_whitespaces():
    def func(cls):
        cls.__accept_whitespaces__ = True
        return cls

    return func
