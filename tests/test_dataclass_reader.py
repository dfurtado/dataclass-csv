import pytest
import dataclasses

from dataclass_csv import DataclassReader, CsvValueError

from .mocks import User, DataclassWithBooleanValue, DataclassWithBooleanValueNoneDefault


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


def test_csv_header_items_with_spaces(create_csv):
    csv_file = create_csv({'  name': 'User1', 'age   ': 40})

    with csv_file.open() as f:
        reader = DataclassReader(f, User)
        items = list(reader)

        assert items and len(items) > 0

        user = items[0]

        assert user.name == 'User1'
        assert user.age == 40


def test_csv_header_items_with_spaces_together_with_skipinitialspaces(create_csv):
    csv_file = create_csv({'  name': 'User1', 'age   ': 40})

    with csv_file.open() as f:
        reader = DataclassReader(f, User, skipinitialspace=True)
        items = list(reader)

        assert items and len(items) > 0

        user = items[0]

        assert user.name == 'User1'
        assert user.age == 40


def test_parse_bool_value_true(create_csv):
    for true_value in ['yes', 'true', 't', 'y', '1']:
        csv_file = create_csv({'boolValue': f'{true_value}'})
        with csv_file.open() as f:
            reader = DataclassReader(f, DataclassWithBooleanValue)
            items = list(reader)
            dataclass_instance = items[0]
            assert dataclass_instance.boolValue is True


def test_parse_bool_value_false(create_csv):
    for false_value in ['no', 'false', 'f', 'n', '0']:
        csv_file = create_csv({'boolValue': f'{false_value}'})
        with csv_file.open() as f:
            reader = DataclassReader(f, DataclassWithBooleanValue)
            items = list(reader)
            dataclass_instance = items[0]
            assert dataclass_instance.boolValue is False


def test_parse_bool_value_invalid(create_csv):
    csv_file = create_csv({'boolValue': 'notValidBoolean'})
    with csv_file.open() as f:
        try:
            reader = DataclassReader(f, DataclassWithBooleanValue)
            list(reader)
            assert False  # Should not be able to successfully parse
        except CsvValueError:
            pass


def test_parse_bool_value_none_default(create_csv):
    """Verify that blank/null values are parsed as None for optional fields"""
    csv_file = create_csv({'boolValue': ''})
    with csv_file.open() as f:
        reader = DataclassReader(f, DataclassWithBooleanValueNoneDefault)
        items = list(reader)
        dataclass_instance = items[0]
        assert dataclass_instance.boolValue is None
