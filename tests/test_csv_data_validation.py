import pytest

from dataclass_csv import DataclassReader, CsvValueError

from .mocks import User, UserWithDateFormatDecorator


def test_should_raise_error_str_to_int_prop(create_csv):
    csv_file = create_csv({'name': 'User1', 'age': 'wrong type'})

    with csv_file.open() as f:
        with pytest.raises(CsvValueError):
            reader = DataclassReader(f, User)
            list(reader)


def test_should_raise_error_with_incorrect_dateformat(create_csv):
    csv_file = create_csv({'name': 'User1', 'create_date': '2018-12-07 10:00'})

    with csv_file.open() as f:
        with pytest.raises(CsvValueError):
            reader = DataclassReader(f, UserWithDateFormatDecorator)
            list(reader)


def test_should_raise_error_when_required_value_is_missing(create_csv):
    csv_file = create_csv({'name': 'User1', 'age': None})

    with csv_file.open() as f:
        with pytest.raises(CsvValueError):
            reader = DataclassReader(f, User)
            list(reader)


def test_should_raise_error_when_required_column_is_missing(create_csv):
    csv_file = create_csv({'name': 'User1'})

    with csv_file.open() as f:
        with pytest.raises(KeyError):
            reader = DataclassReader(f, User)
            list(reader)


def test_should_raise_error_when_required_value_is_emptyspaces(create_csv):
    csv_file = create_csv({'name': '     ', 'age': 40})

    with csv_file.open() as f:
        with pytest.raises(CsvValueError):
            reader = DataclassReader(f, User)
            list(reader)


def test_csv_header_items_with_spaces_with_missing_props_raises_keyerror(create_csv):
    csv_file = create_csv({'  name': 'User1'})

    with csv_file.open() as f:
        with pytest.raises(KeyError):
            reader = DataclassReader(f, User)
            items = list(reader)


def test_csv_header_items_with_spaces_with_missing_value(create_csv):
    csv_file = create_csv({'  name': 'User1', 'age   ': None})

    with csv_file.open() as f:
        with pytest.raises(CsvValueError):
            reader = DataclassReader(f, User)
            items = list(reader)


def test_csv_header_items_with_spaces_with_prop_with_wrong_type(create_csv):
    csv_file = create_csv({'  name': 'User1', 'age   ': 'this should be an int'})

    with csv_file.open() as f:
        with pytest.raises(CsvValueError):
            reader = DataclassReader(f, User)
            items = list(reader)
