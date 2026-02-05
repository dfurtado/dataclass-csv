[![Unit testing](https://github.com/dfurtado/dataclass-csv/actions/workflows/unit-test.yml/badge.svg)](https://github.com/dfurtado/dataclass-csv/actions/workflows/unit-test.yml)
[![pypi](https://img.shields.io/pypi/v/dataclass-csv.svg)](https://pypi.python.org/pypi/dataclass-csv)
[![Downloads](https://pepy.tech/badge/dataclass-csv)](https://pepy.tech/project/dataclass-csv)

# Dataclass CSV

Dataclass CSV makes working with CSV files simpler and more reliable than using dictionaries. It leverages Python’s dataclasses to represent each row in a CSV file, while also supporting type annotations for proper type checking and validation.

## ✨ Key Features

### 📦 Dataclasses instead of dictionaries  
Represent CSV rows as dataclass instances for cleaner, more structured code.

### 🔍 Type‑aware validation  
`DataclassReader` uses type annotations to validate CSV data automatically.

### 🔄 Automatic type conversion  
Supports `str`, `int`, `float`, `complex`, `datetime`, and `bool`, plus any type whose constructor accepts a single string argument.

### 🧭 Detailed error reporting  
Pinpoints exactly which line in the CSV contains invalid data, making troubleshooting easier.

### 🎯 Selective parsing  
Only extracts the fields defined in your dataclass, so you get exactly the data you need.

### 🧩 Familiar syntax  
Works much like Python’s built‑in `csv.DictReader`, so it feels natural to use.

### 🏷️ Metadata support  
Leverages dataclass metadata to customize how data is parsed.

### 🧼 Cleaner code  
Eliminates the need for manual loops to convert types, validate data, or set default values—`DataclassReader` handles it all.

### ✍️ CSV writing support  
Alongside reading, the library provides `DataclassWriter` for generating CSV files from lists of dataclass instances.



## Installation

```shell
pip install dataclass-csv
```

## Getting started

### Using the DataclassReader

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
The dataclass `User` has three properties: `firstname` and `email`, both of type `str`, and `age`, of type `int`.

To load and read the contents of a CSV file, you follow the same approach as when using DictReader from Python’s standard csv module. After opening the file, you create an instance of `DataclassReader`, passing two arguments: the file object and the dataclass you want to use to represent each row of the CSV. For example:

```python
with open(filename) as users_csv:
    reader = DataclassReader(users_csv, User)
    for row in reader:
        print(row)
```

Internally, `DataclassReader` relies on Python’s `csv.DictReader` to read CSV files. This means you can pass the same arguments that you would normally provide to `DictReader`. The full list of supported arguments is shown below:


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

All keyword arguments supported by `DictReader` are also supported by `DataclassReader`, with one additional option:

`validate_header` — When enabled, `DataclassReader` will raise a ValueError if the CSV file contains duplicate column names. This validation helps prevent data from being overwritten. To disable this check, set `validate_header=False` when creating a `DataclassReader` instance. For example:


```python
reader = DataclassReader(f, User, validate_header=False)
```

Executing the code produces the following output:


```python
User(firstname='Elsa', email='elsa@test.com', age=11)
User(firstname='Astor', email='astor@test.com', age=7)
User(firstname='Edit', email='edit@test.com', age=3)
User(firstname='Ella', email='ella@test.com', age=2)
```

### Error handling

One of the key advantages of using `DataclassReader` is its ability to detect when the data types in a CSV file don’t match what your application’s model expects. In such cases, `DataclassReader` provides clear error messages that help you identify exactly which rows contain problematic values.

For example, if we modify the CSV file from the **Getting Started** section and change the age of the user Astor to a string value, the error will highlight this mismatch:

```text
Astor, astor@test.com, test
```
Remember that in the `User` dataclass, the `age` property is annotated as an `int`. If we run the code again, an exception will be raised with the following message:


```text
dataclass_csv.exceptions.CsvValueError: The field `age` is defined as <class 'int'> but
received a value of type <class 'str'>. [CSV Line number: 3]
```

Note that, in addition to describing the error, `DataclassReader` also indicates which line of the CSV file contains the problematic data.


### Default values

`DataclassReader` can process dataclass fields that define default values. As an example, we’ll modify the `User` dataclass to assign a default value to the `email` field:

```python
from dataclasses import dataclass


@dataclass
class User:
    firstname: str
    email: str = 'Not specified'
    age: int
```
We then update the CSV file, removing the email value for the user Astor:

```python
Astor,, 7
```
When you run the code, the output will appear as follows:

```text
User(firstname='Elsa', email='elsa@test.com', age=11)
User(firstname='Astor', email='Not specified', age=7)
User(firstname='Edit', email='edit@test.com', age=3)
User(firstname='Ella', email='ella@test.com', age=2)
```
Note that the `User` object for Astor now has the default value `Not specified` assigned to the email property.

Default values can also be defined using `dataclasses.field`, as shown below:

```python
from dataclasses import dataclass, field


@dataclass
class User:
    firstname: str
    email: str = field(default='Not specified')
    age: int
```

### Mapping dataclass fields to columns

By default, `DataclassReader` automatically maps dataclass properties to CSV columns when their names match. However, there are cases where a column header in the CSV file uses a different name. In such situations, you can explicitly define the mapping using the map method.

For example, consider the following CSV file:

```text
First Name,email,age
Elsa,elsa@test.com, 11
```

Notice that the column header is now **First Name** instead of **firstname**.

To handle this difference, we can use the map method as follows:

```python
reader = DataclassReader(users_csv, User)
reader.map('First name').to('firstname')
```

Now, `DataclassReader` will correctly extract the data from the **First Name** column 
and assign it to the **firstname** property in the dataclass.

### Supported type annotation

Currently, `DataclassReader` supports the following types: `int`, `str`, `float`, `complex`, `datetime`, and `bool`.

When working with a datetime property, you must use the `dateformat` decorator to specify how the date should be parsed. For example:

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

It’s important to note that the `dateformat` decorator defines the date format used to parse all datetime properties in a dataclass. However, CSV files may sometimes contain multiple date columns with different formats. In these cases, you can assign a format specific to each property by using dataclasses.field.

For example, consider the following CSV file:


```text
name,email,birthday, create_date
Edit,edit@test.com,2018/11/23,2018/11/23 10:43
```
As you can see, the `create_date` column includes time information.

The `User` dataclass can be defined as follows:

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

Notice that the `birthday` field does not have a format specified through field metadata. In this case, the format defined in the `dateformat` decorator will be applied.

### Handling values with empty spaces

When defining a property of type `str` in a dataclass, `DataclassReader` treats values that contain only whitespace as invalid.

To change this behavior, you can use the `@accept_whitespaces` decorator. When applied to the class, this decorator allows whitespace-only values to be accepted as valid input. For example:


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

If you need a specific field to accept white spaces, you can set the property `accept_whitespaces` in the field's metadata:

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

Reading CSV files with `DataclassReader` gives you the full benefit of Python’s type‑safety through dataclasses and type annotations. But sometimes we need to go in the opposite direction—using dataclasses to produce CSV output. That’s exactly where `DataclassWriter` shines.

Using `DataclassWriter` is straightforward. Suppose we have a simple `User` dataclass:

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
To generate a CSV file with `DataclassWriter`, start by importing it from `dataclass_csv`:

```python
from dataclass_csv import DataclassWriter
```

Initialize it with the required arguments and call the method `write`:

```python
with open("users.csv", "w+") as f:
    w = DataclassWriter(f, users, User)
    w.write()
```

That’s it! Let’s break down what’s happening in the example above.

We start by opening a file named `user.csv in write mode. Then we create a `DataclassWriter` instance. To initialize a writer, we provide three things: the file object, the list of `User` instances, and the dataclass type itself (`User`).

The type is required because the writer uses it to determine the CSV header. By default, it takes the field names defined in the dataclass. For our `User` example, the resulting column titles are `firstname`, `lastname`, and `age`.

Here’s the CSV generated from the list of `User` objects:

```text
firstname,lastname,age
John,Smith,40
Daniel,Nilsson,10
Ella,Fralla,4
```
`DataclassWriter` also accepts `**fmtparams`, which are passed directly to Python’s built‑in `csv.writer`. You can use this to customize delimiter behavior, quoting, line endings, and other CSV formatting options. For details, see the official CSV documentation: https://docs.python.org/3/library/csv.html#csv-fmt-params

There are also cases where you may want to omit the CSV header. The write method provides a `skip_header` argument for this purpose. It defaults to `False`, but when set to `True`, the writer will skip generating the header row.

#### Modifying the CSV header

As mentioned earlier, `DataclassWriter` uses the dataclass field names as the default CSV header titles. Depending on your use case, you may want to customize these titles. For that, `DataclassWriter` provides the map method.

Using our `User` dataclass with the fields `firstname`, `lastname`, and `age`, the example below shows how to rename `firstname` to `First name` and `lastname` to `Last name`:

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

## Contributors

A heartfelt thank you to all the incredible contributors who have supported this project over the years. Special thanks go to [@kraktus](https://github.com/kraktus) for setting up GitHub Actions, enhancing automation for package creation, and delivering numerous code improvements.

<a href="https://github.com/dfurtado/dataclass-csv/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=dfurtado/dataclass-csv" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## Copyright and License

Copyright (c) 2018 Daniel Furtado. Code released under BSD 3-clause license

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
