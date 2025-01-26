from csv import DictWriter
from typing import Any, Dict, List, Union

import pytest


@pytest.fixture()
def create_csv(tmpdir_factory):
    def func(data: Union[Dict[str, Any], List[Dict[str, Any]]], fieldnames=None, filename="user.csv", factory=tmpdir_factory):

        assert data

        file = tmpdir_factory.mktemp("data").join(filename)

        row = data[0] if isinstance(data, list) else data

        header = fieldnames if fieldnames is not None else row.keys()

        with file.open("w") as f:
            writer = DictWriter(f, fieldnames=header)
            writer.writeheader()
            if isinstance(data, list):
                writer.writerows(data)
            else:
                writer.writerow(data)

        return file

    return func
