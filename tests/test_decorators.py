import pytest

from dataclass_csv import DataclassReader, CsvValueError

from .mocks import (
    UserWithoutDateFormatDecorator,
    UserWithDateFormatDecorator,
    UserWithDateFormatMetadata,
    UserWithDateFormatDecoratorAndMetadata,
    UserWithoutAcceptWhiteSpacesDecorator,
    UserWithAcceptWhiteSpacesDecorator,
    UserWithAcceptWhiteSpacesMetadata,
)


def test_should_raise_error_without_dateformat(create_csv):
    csv_file = create_csv({'name': 'Test', 'create_date': '2018-12-09'})

    with csv_file.open('r') as f:
        with pytest.raises(AttributeError):
            reader = DataclassReader(f, UserWithoutDateFormatDecorator)
            list(reader)


def test_shold_not_raise_error_when_using_dateformat_decorator(create_csv):
    csv_file = create_csv({'name': 'Test', 'create_date': '2018-12-09'})

    with csv_file.open('r') as f:
        reader = DataclassReader(f, UserWithDateFormatDecorator)
        list(reader)


def test_shold_not_raise_error_when_dateformat_metadata(create_csv):
    csv_file = create_csv({'name': 'Test', 'create_date': '2018-12-09'})

    with csv_file.open('r') as f:
        reader = DataclassReader(f, UserWithDateFormatMetadata)
        list(reader)


def test_use_decorator_when_metadata_is_not_defined(create_csv):
    csv_file = create_csv(
        {
            'name': 'Test',
            'birthday': '1977-08-26',
            'create_date': '2018-12-09 11:11',
        }
    )

    with csv_file.open('r') as f:
        reader = DataclassReader(f, UserWithDateFormatDecoratorAndMetadata)
        list(reader)


def test_should_raise_error_when_value_is_whitespaces(create_csv):
    csv_file = create_csv({'name': '     '})

    with csv_file.open('r') as f:
        with pytest.raises(CsvValueError):
            reader = DataclassReader(f, UserWithoutAcceptWhiteSpacesDecorator)
            list(reader)


def test_should_not_raise_error_when_value_is_whitespaces(create_csv):
    csv_file = create_csv({'name': '     '})

    with csv_file.open('r') as f:
        reader = DataclassReader(f, UserWithAcceptWhiteSpacesDecorator)
        data = list(reader)

        user = data[0]
        assert user.name == '     '


def test_should_not_raise_error_when_using_meta_accept_whitespaces(create_csv):
    csv_file = create_csv({'name': '     '})

    with csv_file.open('r') as f:
        reader = DataclassReader(f, UserWithAcceptWhiteSpacesMetadata)
        data = list(reader)

        user = data[0]
        assert user.name == '     '
