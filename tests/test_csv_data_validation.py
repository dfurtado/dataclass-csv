import pytest
import dataclasses

from datetime import datetime

from dataclass_csv import DataclassReader


@dataclasses.dataclass
class User:
    name: str
    age: int


@dataclasses.dataclass
class UserWithoutDateFormat:
    name: str
    create_date: datetime


@dataclasses.dataclass
class UserWithDateFormat:
    name: str
    create_date: datetime = dataclasses.field(
        metadata={'dateformat': '%Y-%m-%d'}
    )


def test_should_raise_error_str_to_int_prop(create_csv):
    csv_file = create_csv({'name': 'User1', 'age': 'wrong type'})

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            reader = DataclassReader(f, User)
            data = list(reader)


def test_should_raise_error_dataclass_without_dateformat(create_csv):
    csv_file = create_csv({'name': 'User1', 'create_date': '2018-12-07'})

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            reader = DataclassReader(f, UserWithoutDateFormat)
            data = list(reader)


def test_should_not_raise_error_dataclass_with_dateformat(create_csv):
    csv_file = create_csv({'name': 'User1', 'create_date': '2018-12-07'})

    with csv_file.open() as f:
        reader = DataclassReader(f, UserWithDateFormat)
        data = list(reader)


def test_should_raise_error_with_incorrect_dateformat(create_csv):
    csv_file = create_csv({'name': 'User1', 'create_date': '2018-12-07 10:00'})

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            reader = DataclassReader(f, UserWithDateFormat)
            data = list(reader)


def test_should_raise_error_when_required_value_is_missing(create_csv):
    csv_file = create_csv({'name': 'User1', 'age': None})

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            reader = DataclassReader(f, User)
            data = list(reader)


def test_should_raise_error_when_required_column_is_missing(create_csv):
    csv_file = create_csv({'name': 'User1'})

    with csv_file.open() as f:
        with pytest.raises(KeyError):
            reader = DataclassReader(f, User)
            data = list(reader)


def test_should_raise_error_when_required_value_is_emptyspaces(create_csv):
    csv_file = create_csv({'name': '     ', 'age': 40})

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            reader = DataclassReader(f, User)
            data = list(reader)
