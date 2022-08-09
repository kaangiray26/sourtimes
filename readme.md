# sourtimes
The Python Eksisozluk API Wrapper

## Documentation
Coming soon...

## Installation
```
git clone https://github.com/kgbzen/sourtimes.git
cd sourtimes
python -m pip install -r requirements.txt
```

## Quickstart
```
from sourtimes import sour

eksi = sour()
q = eksi.autocomplete("uzun a")
print(q.titles)
```