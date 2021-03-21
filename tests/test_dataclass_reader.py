import pytest
import dataclasses

from datetime import datetime
from dataclass_csv import DataclassReader, CsvValueError

from .mocks import (
    User,
    UserWithOptionalAge,
    DataclassWithBooleanValue,
    DataclassWithBooleanValueNoneDefault,
    UserWithInitFalse,
    UserWithInitFalseAndDefaultValue,
    UserWithDefaultDatetimeField,
    UserWithSSN,
    SSN,
    UserWithEmail,
)


def test_reader_with_non_dataclass(create_csv):
    csv_file = create_csv({"name": "User1", "age": 40})

    class DummyUser:
        pass

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            DataclassReader(f, DummyUser)


def test_reader_with_none_class(create_csv):
    csv_file = create_csv({"name": "User1", "age": 40})

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            DataclassReader(f, None)


def test_reader_with_none_file():
    with pytest.raises(ValueError):
        DataclassReader(None, User)


def test_reader_with_correct_values(create_csv):
    csv_file = create_csv({"name": "User", "age": 40})

    with csv_file.open() as f:
        reader = DataclassReader(f, User)
        list(reader)


def test_reader_values(create_csv):
    csv_file = create_csv([{"name": "User1", "age": 40}, {"name": "User2", "age": 30}])

    with csv_file.open() as f:
        reader = DataclassReader(f, User)
        items = list(reader)

        assert items and len(items) == 2

        for item in items:
            assert dataclasses.is_dataclass(item)

        user1, user2 = items[0], items[1]

        assert user1.name == "User1"
        assert user1.age == 40

        assert user2.name == "User2"
        assert user2.age == 30


def test_csv_header_items_with_spaces(create_csv):
    csv_file = create_csv({"  name": "User1", "age   ": 40})

    with csv_file.open() as f:
        reader = DataclassReader(f, User)
        items = list(reader)

        assert items and len(items) > 0

        user = items[0]

        assert user.name == "User1"
        assert user.age == 40


def test_csv_header_items_with_spaces_together_with_skipinitialspaces(create_csv):
    csv_file = create_csv({"  name": "User1", "age   ": 40})

    with csv_file.open() as f:
        reader = DataclassReader(f, User, skipinitialspace=True)
        items = list(reader)

        assert items and len(items) > 0

        user = items[0]

        assert user.name == "User1"
        assert user.age == 40


def test_parse_bool_value_true(create_csv):
    for true_value in ["yes", "true", "t", "y", "1"]:
        csv_file = create_csv({"boolValue": f"{true_value}"})
        with csv_file.open() as f:
            reader = DataclassReader(f, DataclassWithBooleanValue)
            items = list(reader)
            dataclass_instance = items[0]
            assert dataclass_instance.boolValue is True


def test_parse_bool_value_false(create_csv):
    for false_value in ["no", "false", "f", "n", "0"]:
        csv_file = create_csv({"boolValue": f"{false_value}"})
        with csv_file.open() as f:
            reader = DataclassReader(f, DataclassWithBooleanValue)
            items = list(reader)
            dataclass_instance = items[0]
            assert dataclass_instance.boolValue is False


def test_parse_bool_value_invalid(create_csv):
    csv_file = create_csv({"boolValue": "notValidBoolean"})
    with csv_file.open() as f:
        with pytest.raises(CsvValueError):
            reader = DataclassReader(f, DataclassWithBooleanValue)
            list(reader)


def test_parse_bool_value_none_default(create_csv):
    csv_file = create_csv({"boolValue": ""})
    with csv_file.open() as f:
        reader = DataclassReader(f, DataclassWithBooleanValueNoneDefault)
        items = list(reader)
        dataclass_instance = items[0]
        assert dataclass_instance.boolValue is None


def test_skip_dataclass_field_when_init_is_false(create_csv):
    csv_file = create_csv({"firstname": "User1", "lastname": "TestUser"})
    with csv_file.open() as f:
        reader = DataclassReader(f, UserWithInitFalse)
        list(reader)


def test_try_to_access_not_initialized_prop_raise_attr_error(create_csv):
    csv_file = create_csv({"firstname": "User1", "lastname": "TestUser"})
    with csv_file.open() as f:
        reader = DataclassReader(f, UserWithInitFalse)
        items = list(reader)
        with pytest.raises(AttributeError):
            user = items[0]
            assert user.age is not None


def test_try_to_access_not_initialized_prop_with_default_value(create_csv):
    csv_file = create_csv({"firstname": "User1", "lastname": "TestUser"})
    with csv_file.open() as f:
        reader = DataclassReader(f, UserWithInitFalseAndDefaultValue)
        items = list(reader)
        user = items[0]
        assert user.age == 0


def test_reader_with_optional_types(create_csv):
    csv_file = create_csv({"name": "User", "age": 40})

    with csv_file.open() as f:
        reader = DataclassReader(f, UserWithOptionalAge)
        list(reader)


def test_reader_with_datetime_default_value(create_csv):
    csv_file = create_csv({"name": "User", "birthday": ""})

    with csv_file.open() as f:
        reader = DataclassReader(f, UserWithDefaultDatetimeField)
        items = list(reader)
        assert len(items) > 0
        assert isinstance(items[0].birthday, datetime)


def test_should_parse_user_defined_types(create_csv):
    csv_file = create_csv(
        [
            {"name": "User1", "ssn": "123-45-6789"},
            {"name": "User1", "ssn": "123456789"},
        ]
    )

    with csv_file.open() as f:
        reader = DataclassReader(f, UserWithSSN)
        items = list(reader)
        assert len(items) == 2

        assert isinstance(items[0].ssn, SSN)
        assert items[0].ssn.val == "123-45-6789"

        assert isinstance(items[1].ssn, SSN)
        assert items[1].ssn.val == "123-45-6789"


def test_raise_error_when_mapped_column_not_found(create_csv):
    csv_file = create_csv({"name": "User1", "e-mail": "test@test.com"})

    with csv_file.open() as f:
        with pytest.raises(
            KeyError,
            match="The value for the mapped column `e_mail` is missing in the CSV file",
        ):
            reader = DataclassReader(f, UserWithEmail)
            reader.map("e_mail").to("email")
            list(reader)


def test_raise_error_when_field_not_found(create_csv):
    csv_file = create_csv({"name": "User1", "e-mail": "test@test.com"})

    with csv_file.open() as f:
        with pytest.raises(
            KeyError,
            match="The value for the column `email` is missing in the CSV file.",
        ):
            reader = DataclassReader(f, UserWithEmail)
            list(reader)


def test_raise_error_when_duplicate_header_items(create_csv):
    csv_file = create_csv(
        {"name": "User1", "email": "test@test.com"},
        fieldnames=["name", "email", "name"],
    )

    with csv_file.open() as f:
        with pytest.raises(ValueError):
            reader = DataclassReader(f, UserWithEmail)
            list(reader)


def test_skip_header_validation(create_csv):
    csv_file = create_csv(
        {"name": "User1", "email": "test@test.com"},
        fieldnames=["name", "email", "name"],
    )

    with csv_file.open() as f:
        reader = DataclassReader(f, UserWithEmail, validate_header=False)
        list(reader)
