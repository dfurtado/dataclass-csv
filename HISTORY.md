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
