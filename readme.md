# sourpy
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
git clone https://github.com/kgbzen/sourpy.git
cd sourpy
python -m pip install -r requirements.txt
```

## Quickstart
```
from sourpy import Sour

eksi = Sour()
q = eksi.autocomplete("uzun a")
print(q.titles)
```