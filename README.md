# sourtimes
The Python Eksisozluk API Wrapper

## Features
* Get autocomplete results
* Get ```gündem``` titles
* Get ```debe``` titles
* Search for titles with parameters
* Get entries from a page

## Documentation
Coming soon...

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