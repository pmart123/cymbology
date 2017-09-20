class IdError(Exception): pass


class NullError(IdError): pass


class InvalidCharacterError(IdError):
    """Input contains invalid characters base on identifer specification."""


class CheckDigitError(IdError):
    """Check digit does not match rest of identifer input."""


class CheckSumError(IdError):
    """The check digit does not equal the check sum."""


class CountryCodeError(IdError):
    """Part of the identifier should match an ISO country code."""


class LengthError(IdError):
    """Invalid length input for identifer."""
