# Dataclass CSV

Dataclass CSV makes working with CSV files easier and much better than working with Dicts. It uses Python's Dataclasses to store data of every row on the CSV file and also uses type annotations which enables proper type checking and validation.

## Installation

```shell
pipenv install dataclass-csv
```

## Getting started

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
class User():
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
dataclass_csv.DataclassReader(f, cls, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds)
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

For example, say we change the contents of the CSV file shown in the Getting started section and, modify the `age` of the user Astor, let's change it to a string value:

```text
Astor, astor@test.com, test
```

Remember that in the dataclass `User` the `age` property is annotated with `int`. If we run the code again an exception will be raised with the message below:

```python
ValueError: The field age is of type <class 'int'> but received a value of type <class 'str'>
```

### Default values

The `DataclassReader` also handles properties with default values. Let's modify the dataclass `User` and add a default value for the field `email`:

```python
class User():
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

## Copyright and License

Copyright (c) 2018 Daniel Furtado. Code released under BSD 3-clause license

## Credits

This package was created with Cookiecutter and the audreyr/cookiecutter-pypackage project template.
