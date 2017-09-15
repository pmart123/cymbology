# cymbology
cymbology identifies and validates financial security ids.  Currently the following identifiers are supported:

1. Sedol
2. Cusip
3. Isin


This package can be used to validate these identifiers, discover the validation error, or create checksum digits.

# Example Usage:

### ISIN number
```python
from cymbology import Isin, cusip_from_isin
isin = Isin()

# validate ISIN number 'US0378331005', throwing error IdError if invalid
>>> valid_isin = isin.validate('US0378331005')
>>> valid_isin
'US0378331005'
    
# return validation boolean for ISIN number
>>> tf = isin.is_valid('US0378331005')
>>> tf
True
    
# calculate checksum for ISIN number 'US0378331005'
check_digit = isin.calculate_checksum('US037833100')

# convert ISIN to CUSIP number.
>>> cusip_from_isin('US0378331005')
'037833100'
```

# Dependancies and Installation Notes

This package currently only relies on the standard library, and has not been tested for Python 2.X.

# Running Tests

PYTHONPATH=. py.test --cov

# Extending

Idenifiers that rely on alpha-numeric codes should be able to be easily extended.  Feel free to add additional identification algorithmns.  Legal Indenifiers(LEI) ids will be added to master branch of repo soon.
