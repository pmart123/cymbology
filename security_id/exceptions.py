
class IdError(Exception): pass
class NullError(IdError): pass
class CheckDigitError(IdError): pass
class LengthError(IdError): pass
class CountryCodeError(IdError): pass
class CharacterError(IdError): pass
class CheckSumError(IdError): pass