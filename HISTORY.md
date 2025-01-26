# History

### 0.1.0 (2025-01-26)

* First release on PyPI, based on version 1.4.0 of [dataclass-csv](https://github.com/dfurtado/dataclass-csv).
* Remove dependency on `distutils` which is longer bundled with python starting from 3.12.
* Support all iterables instead of just List as input to `DataclassWriter`.
* Add return type hints `DataclassReader` methods.