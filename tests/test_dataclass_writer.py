import pytest

from dataclass_csv import DataclassWriter, DataclassReader

from .mocks import User, SimpleUser, NonDataclassUser


def test_create_csv_file(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with tempfile.open("w") as f:
        w = DataclassWriter(f, users, User)
        w.write()

    with tempfile.open() as f:
        reader = DataclassReader(f, User)
        saved_users = list(reader)

        assert len(saved_users) > 0
        assert saved_users[0].name == users[0].name


def test_wrong_type_items(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with tempfile.open("w") as f:
        with pytest.raises(TypeError):
            w = DataclassWriter(f, users, SimpleUser)
            w.write()


def test_with_a_non_dataclass(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with tempfile.open("w") as f:
        with pytest.raises(ValueError):
            DataclassWriter(f, users, NonDataclassUser)


def test_with_a_empty_cls_value(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with tempfile.open("w") as f:
        with pytest.raises(ValueError):
            DataclassWriter(f, users, None) # type: ignore


def test_invalid_file_value(tmpdir_factory):
    tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with pytest.raises(ValueError):
        DataclassWriter(None, users, User)

def test_with_iterable(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")
    users_dict = {"test": User(name="test", age=40)}

    with tempfile.open("w") as f:
        DataclassWriter(f, users_dict.values(), User).write()

    with tempfile.open() as f:
        reader = DataclassReader(f, User)
        saved_users = list(reader)

        assert len(saved_users) > 0
        assert saved_users[0].name == users_dict["test"].name
