![PyPI](https://img.shields.io/pypi/v/sourtimes?color=blue)
[![GitHub license](https://img.shields.io/github/license/kgbzen/sourtimes)](https://github.com/kgbzen/sourtimes/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/kgbzen/sourtimes)](https://github.com/kgbzen/sourtimes/issues)

The Python Eksisozluk API Wrapper

## Features
* Get autocomplete results
* Get ```gündem``` titles
* Get ```debe``` titles
* Search for titles with parameters
* Get entries from a page

## Documentation
https://sourtimes.readthedocs.io/

## PyPI
https://pypi.org/project/sourtimes/

## Installation
```
pip install sourtimes
```

## Quickstart
```
from sourtimes import Sour

eksi = Sour()
q = eksi.autocomplete("uzun a")
print(q.titles)
```
