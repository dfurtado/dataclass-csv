# History

### 0.1.0 (2018-11-25)

* First release on PyPI.

### 0.1.1 (2018-11-25)

* Documentation fixes.

### 0.1.2 (2018-11-25)

* Documentation fixes.

### 0.1.3 (2018-11-26)

* Bug fixes
* Removed the requirement of setting the dataclass init to `True`

### 0.1.5 (2018-11-29)

* Support for parsing datetime values.
* Better handling when default values are set to `None`

### 0.1.6 (2018-12-01)

* Added support for reader default values from the default property of the `dataclasses.field`.
* Added support for allowing string values with only white spaces in a class level using the `@accept_whitespaces` decorator or through the `dataclasses.field` metadata.
* Added support for specifying date format using the `dataclasses.field` metadata.

### 0.1.7 (2018-12-01)

* Added support for default values from `default_factory` in the field's metadata. This allows adding mutable default values to the dataclass properties.

### 1.0.0 (2018-12-16)

* When a data does not pass validation it shows the line number in the CSV file where the data contain errors.
* Improved error handling.
* Changed the usage of the `@accept_whitespaces` decorator.
* Updated documentation.

### 1.0.1 (2019-01-29)

* Fixed issue when parsing headers on a CSV file with trailing white spaces.

### 1.1.0 (2019-02-17)

* Added support for boolean values.
* Docstrings

### 1.1.1 (2019-02-17)

* Documentation fixes.

### 1.1.2 (2019-02-17)

* Documentation fixes.

### 1.1.3 (2020-03-01)

* Handle properties with init set to False
* Handle Option type annotation

### 1.2.0 (2021-03-02)

* Introduction of a DataclassWriter
* Added type hinting to external API
* Documentation updates
* Bug fixes

## 1.3.0 (2021-04-10)

* Included stub files
* check if the CSV file has duplicated header values
* Fixed issues #22 and #33
* code cleanup

