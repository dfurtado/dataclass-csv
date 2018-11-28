def dateformat(date_format):

    if not date_format or not isinstance(date_format, str):
        raise ValueError('Invalid value for the date_format argument')

    def func(cls):
        cls.__date_format__ = date_format
        return cls

    return func
