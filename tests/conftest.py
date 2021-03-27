from csv import DictWriter

import pytest


@pytest.fixture()
def create_csv(tmpdir_factory):
    def func(data, fieldnames=None, filename="user.csv", factory=tmpdir_factory):

        assert data

        file = tmpdir_factory.mktemp("data").join(filename)

        row = data[0] if isinstance(data, list) else data

        header = fieldnames if fieldnames is not None else row.keys()

        with file.open("w") as f:
            writer = DictWriter(f, fieldnames=header)
            writer.writeheader()
            addrow = writer.writerows if isinstance(data, list) else writer.writerow
            addrow(data)

        return file

    return func
