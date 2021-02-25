import pytest
import dataclasses

from dataclass_csv import DataclassWriter, DataclassReader

from .mocks import User, SimpleUser, NonDataclassUser

@pytest.mark.writer
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

@pytest.mark.writer
def test_wrong_type_items(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with tempfile.open("w") as f:
        with pytest.raises(TypeError):
            w = DataclassWriter(f, users, SimpleUser)
            w.write()

@pytest.mark.writer
def test_with_a_non_dataclass(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with tempfile.open("w") as f:
        with pytest.raises(ValueError):
            w = DataclassWriter(f, users, NonDataclassUser)

@pytest.mark.writer
def test_with_a_empty_cls_value(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with tempfile.open("w") as f:
        with pytest.raises(ValueError):
            w = DataclassWriter(f, users, None)

@pytest.mark.writer
def test_invalid_file_value(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = [User(name="test", age=40)]

    with pytest.raises(ValueError):
        w = DataclassWriter(None, users, User)

@pytest.mark.writer
def test_with_data_not_a_list(tmpdir_factory):
    tempfile = tmpdir_factory.mktemp("data").join("user_001.csv")

    users = User(name="test", age=40)

    with tempfile.open("w") as f:
        with pytest.raises(ValueError):
            w = DataclassWriter(f, users, User)

