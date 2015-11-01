# security_id
security_id identifies and validates financial security ids.  Currently the following identifiers are supported:

1. Sedol
2. Cusip
3. Isin


This package can be used to validate these identifiers, discover the validation error, or create checksum digits.

# Example Usage:

### ISIN number
```python
from security_id import validation
isin = validation.Isin()

# validate ISIN number 'US0378331005', throwing error IdError if invalid
tf = isin.validate('US0378331005')

# return validation boolean for ISIN number
tr = isin.is_valid('US0378331005')

# calculate checksum for ISIN number 'US0378331005'
check_digit = isin.calculate_checksum('US037833100')

```

# Dependancies and Installation Notes

This package currently only relies on the standard library, and has not been tested for Python 2.X.

# Extending

Idenifiers that rely on alpha-numeric codes should be able to be easily extended.  Feel free to add additional identification algorithmns.  Legal Indenifiers(LEI) ids will be added to master branch of repo soon.
