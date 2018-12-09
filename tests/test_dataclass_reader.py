import pytest
import dataclasses

from dataclass_csv import DataclassReader

from .mocks import User


def test_reader_with_non_dataclass(create_csv):
    csv_file = create_csv({'name': 'User1', 'age': 40})

    class DummyUser:
        pass

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            DataclassReader(f, DummyUser)


def test_reader_with_none_class(create_csv):
    csv_file = create_csv({'name': 'User1', 'age': 40})

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            DataclassReader(f, None)


def test_reader_with_none_file():

    with pytest.raises(ValueError):
        DataclassReader(None, User)


def test_reader_with_correct_values(create_csv):
    csv_file = create_csv({'name': 'User', 'age': 40})

    with csv_file.open() as f:
        reader = DataclassReader(f, User)
        list(reader)


def test_reader_values(create_csv):
    csv_file = create_csv(
        [{'name': 'User1', 'age': 40}, {'name': 'User2', 'age': 30}]
    )

    with csv_file.open() as f:
        reader = DataclassReader(f, User)
        items = list(reader)

        assert items and len(items) == 2

        for item in items:
            assert dataclasses.is_dataclass(item)

        user1, user2 = items[0], items[1]

        assert user1.name == 'User1'
        assert user1.age == 40

        assert user2.name == 'User2'
        assert user2.age == 30
