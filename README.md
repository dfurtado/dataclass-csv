[![Build Status](https://travis-ci.org/dfurtado/dataclass-csv.svg?branch=master)](https://travis-ci.org/dfurtado/dataclass-csv)
[![pypi](https://img.shields.io/pypi/v/dataclass-csv.svg)](https://pypi.python.org/pypi/dataclass-csv)
[![Downloads](https://pepy.tech/badge/dataclass-csv)](https://pepy.tech/project/dataclass-csv)



# Dataclass CSV

Dataclass CSV makes working with CSV files easier and much better than working with Dicts. It uses Python's Dataclasses to store data of every row on the CSV file and also uses type annotations which enables proper type checking and validation.


## Main features

- Use `dataclasses` instead of dictionaries to represent the rows in the CSV file.
- Take advantage of the `dataclass` properties type annotation. `DataclassReader` use the type annotation to perform validation of the data of the CSV file.
- Automatic type conversion. `DataclassReader` supports `str`, `int`, `float`, `complex`, `datetime` and `bool`, as well as any type whose constructor accepts a string as its single argument.
- Helps you troubleshoot issues with the data in the CSV file. `DataclassReader` will show exactly in which line of the CSV file contain errors.
- Extract only the data you need. It will only parse the properties defined in the `dataclass`
- Familiar syntax. The `DataclassReader` is used almost the same way as the `DictReader` in the standard library.
- It uses `dataclass` features that let you define metadata properties so the data can be parsed exactly the way you want.
- Make the code cleaner. No more extra loops to convert data to the correct type, perform validation, set default values, the `DataclassReader` will do all this for you.
- In additon of the `DataclassReader` the library also provides a `DataclassWriter` which enables creating a CSV file
using a list of instances of a dataclass.


## Installation

```shell
pipenv install dataclass-csv
```

## Getting started

## Using the DataclassReader

First, add the necessary imports:

```python
from dataclasses import dataclass

from dataclass_csv import DataclassReader
```

Assuming that we have a CSV file with the contents below:
```text
firstname,email,age
Elsa,elsa@test.com, 11
Astor,astor@test.com, 7
Edit,edit@test.com, 3
Ella,ella@test.com, 2
```

Let's create a dataclass that will represent a row in the CSV file above:
```python
@dataclass
class User:
    firstname: str
    email: str
    age: int
```

The dataclass `User` has 3 properties, `firstname` and `email` is of type `str` and `age` is of type `int`.

To load and read the contents of the CSV file we do the same thing as if we would be using the `DictReader` from the `csv` module in the Python's standard library. After opening the file we create an instance of the `DataclassReader` passing two arguments. The first is the `file` and the second is the dataclass that we wish to use to represent the data of every row of the CSV file. Like so:

```python
with open(filename) as users_csv:
    reader = DataclassReader(users_csv, User)
    for row in reader:
        print(row)
```

The `DataclassReader` internally uses the `DictReader` from the `csv` module to read the CSV file which means that you can pass the same arguments that you would pass to the `DictReader`. The complete argument list is shown below:

```python
dataclass_csv.DataclassReader(
    f,
    cls,
    fieldnames=None,
    restkey=None,
    restval=None,
    dialect='excel',
    *args,
    **kwds
)
```

All keyword arguments support by `DictReader` are supported by the `DataclassReader`, with the addition of:

`validate_header` - The `DataclassReader` will raise a `ValueError` if the CSV file cointain columns with the same name. This
validation is performed to avoid data being overwritten. To skip this validation set `validate_header=False` when creating a
instance of the `DataclassReader`, see an example below:

```python
reader = DataclassReader(f, User, validate_header=False)
```

If you run this code you should see an output like this:

```python
User(firstname='Elsa', email='elsa@test.com', age=11)
User(firstname='Astor', email='astor@test.com', age=7)
User(firstname='Edit', email='edit@test.com', age=3)
User(firstname='Ella', email='ella@test.com', age=2)
```

### Error handling

One of the advantages of using the `DataclassReader` is that it makes it easy to detect when the type of data in the CSV file is not what your application's model is expecting. And, the `DataclassReader` shows errors that will help to identify the rows with problem in your CSV file.

For example, say we change the contents of the CSV file shown in the **Getting started** section and, modify the `age` of the user Astor, let's change it to a string value:

```text
Astor, astor@test.com, test
```

Remember that in the dataclass `User` the `age` property is annotated with `int`. If we run the code again an exception will be raised with the message below:

```text
dataclass_csv.exceptions.CsvValueError: The field `age` is defined as <class 'int'> but
received a value of type <class 'str'>. [CSV Line number: 3]
```

Note that apart from telling what the error was, the `DataclassReader` will also show which line of the CSV file contain the data with errors.

### Default values

The `DataclassReader` also handles properties with default values. Let's modify the dataclass `User` and add a default value for the field `email`:

```python
from dataclasses import dataclass


@dataclass
class User:
    firstname: str
    email: str = 'Not specified'
    age: int
```

And we modify the CSV file and remove the email for the user Astor:

```python
Astor,, 7
```

If we run the code we should see the output below:

```text
User(firstname='Elsa', email='elsa@test.com', age=11)
User(firstname='Astor', email='Not specified', age=7)
User(firstname='Edit', email='edit@test.com', age=3)
User(firstname='Ella', email='ella@test.com', age=2)
```

Note that now the object for the user Astor have the default value `Not specified` assigned to the email property.

Default values can also be set using `dataclasses.field` like so:

```python
from dataclasses import dataclass, field


@dataclass
class User:
    firstname: str
    email: str = field(default='Not specified')
    age: int
```

### Mapping dataclass fields to columns

The mapping between a dataclass property and a column in the CSV file will be done automatically if the names match, however, there are situations that the name of the header for a column is different. We can easily tell the `DataclassReader` how the mapping should be done using the method `map`. Assuming that we have a CSV file with the contents below:

```text
First Name,email,age
Elsa,elsa@test.com, 11
```

Note that now, the column is called **First Name** and not **firstname**

And we can use the method `map`, like so:

```python
reader = DataclassReader(users_csv, User)
reader.map('First name').to('firstname')
```

Now the DataclassReader will know how to extract the data from the column **First Name** and add it to the to dataclass property **firstname**

### Supported type annotation

At the moment the `DataclassReader` support `int`, `str`, `float`, `complex`, `datetime`, and `bool`. When defining a `datetime` property, it is necessary to use the `dateformat` decorator, for example:

```python
from dataclasses import dataclass
from datetime import datetime

from dataclass_csv import DataclassReader, dateformat


@dataclass
@dateformat('%Y/%m/%d')
class User:
    name: str
    email: str
    birthday: datetime


if __name__ == '__main__':

    with open('users.csv') as f:
        reader = DataclassReader(f, User)
        for row in reader:
            print(row)
```

Assuming that the CSV file have the following contents:

```text
name,email,birthday
Edit,edit@test.com,2018/11/23
```

The output would look like this:

```text
User(name='Edit', email='edit@test.com', birthday=datetime.datetime(2018, 11, 23, 0, 0))
```

### Fields metadata

It is important to note that the `dateformat` decorator will define the date format that will be used to parse date to all properties
in the class. Now there are situations where the data in a CSV file contains two or more columns with date values in different formats. It is possible
to set a format specific for every property using the `dataclasses.field`. Let's say that we now have a CSV file with the following contents:

```text
name,email,birthday, create_date
Edit,edit@test.com,2018/11/23,2018/11/23 10:43
```

As you can see the `create_date` contains time information as well.

The `dataclass` User can be defined like this:

```python
from dataclasses import dataclass, field
from datetime import datetime

from dataclass_csv import DataclassReader, dateformat


@dataclass
@dateformat('%Y/%m/%d')
class User:
    name: str
    email: str
    birthday: datetime
    create_date: datetime = field(metadata={'dateformat': '%Y/%m/%d %H:%M'})
```

Note that the format for the `birthday` field was not speficied using the `field` metadata. In this case the format specified in the `dateformat`
decorator will be used.

### Handling values with empty spaces

When defining a property of type `str` in the `dataclass`, the `DataclassReader` will treat values with only white spaces as invalid. To change this
behavior, there is a decorator called `@accept_whitespaces`. When decorating the class with the `@accept_whitespaces` all the properties in the class
will accept values with only white spaces.

For example:

```python
from dataclass_csv import DataclassReader, accept_whitespaces

@accept_whitespaces
@dataclass
class User:
    name: str
    email: str
    birthday: datetime
    created_at: datetime
```

If you need a specific field to accept white spaces, you can set the property `accept_whitespaces` in the field's metadata, like so:

```python
@dataclass
class User:
    name: str
    email: str = field(metadata={'accept_whitespaces': True})
    birthday: datetime
    created_at: datetime
```

### User-defined types

You can use any type for a field as long as its constructor accepts a string:

```python
class SSN:
    def __init__(self, val):
        if re.match(r"\d{9}", val):
            self.val = f"{val[0:3]}-{val[3:5]}-{val[5:9]}"
        elif re.match(r"\d{3}-\d{2}-\d{4}", val):
            self.val = val
        else:
            raise ValueError(f"Invalid SSN: {val!r}")


@dataclasses.dataclass
class User:
    name: str
    ssn: SSN
```


## Using the DataclassWriter

Reading a CSV file using the `DataclassReader` is great and gives us the type-safety of Python's dataclasses and type annotation, however, there are situations where we would like to use dataclasses for creating CSV files, that's where the `DataclassWriter` comes in handy.

Using the `DataclassWriter` is quite simple. Given that we have a dataclass `User`:

```python
from dataclasses import dataclass


@dataclass
class User:
    firstname: str
    lastname: str
    age: int
```

And in your program we have a list of users:

```python

users = [
    User(firstname="John", lastname="Smith", age=40),
    User(firstname="Daniel", lastname="Nilsson", age=10),
    User(firstname="Ella", "Fralla", age=4)
]
```

In order to create a CSV using the `DataclassWriter` import it from `dataclass_csv`:

```python
from dataclass_csv import DataclassWriter
```

Initialize it with the required arguments and call the method `write`:

```python
with open("users.csv", "w") as f:
    w = DataclassWriter(f, users, User)
    w.write()
```

That's it! Let's break down the snippet above.

First, we open a file called `user.csv` for writing. After that, an instance of the `DataclassWriter` is created. To create a `DataclassWriter` we need to pass the `file`, the list of `User` instances, and lastly, the type, which in this case is `User`.

The type is required since the writer uses it when trying to figure out the CSV header. By default, it will use the names of the
properties defined in the dataclass, in the case of the dataclass `User` the title of each column
will be `firstname`, `lastname` and `age`.

See below the CSV created out of a list of `User`:

```text
firstname,lastname,age
John,Smith,40
Daniel,Nilsson,10
Ella,Fralla,4
```

The `DataclassWriter` also takes a `**fmtparams` which accepts the same parameters as the `csv.writer`, for more
information see: https://docs.python.org/3/library/csv.html#csv-fmt-params

Now, there are situations where we don't want to write the CSV header. In this case, the method `write` of
the `DataclassWriter` accepts an extra argument, called `skip_header`. The default value is `False` and when set to
`True` it will skip the header.

#### Modifying the CSV header

As previously mentioned the `DataclassWriter` uses the names of the properties defined in the dataclass as the CSV header titles, however,
depending on your use case it makes sense to change it. The `DataclassWriter` has a `map` method just for this purpose.

 Using the `User` dataclass with the properties `firstname`, `lastname` and `age`. The snippet below shows how to change `firstname` to `First name` and `lastname` to `Last name`:

 ```python
 with open("users.csv", "w") as f:
    w = DataclassWriter(f, users, User)

    # Add mappings for firstname and lastname
    w.map("firstname").to("First name")
    w.map("lastname").to("Last name")

    w.write()
 ```

 The CSV output of the snippet above will be:

```text
First name,Last name,age
John,Smith,40
Daniel,Nilsson,10
Ella,Fralla,4
```

## Copyright and License

Copyright (c) 2018 Daniel Furtado. Code released under BSD 3-clause license

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
