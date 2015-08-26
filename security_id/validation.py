
import string
from abc import ABCMeta,abstractmethod
from itertools import chain
from math import isnan

from security_id.codes import CINS_CODES,COUNTRY_CODES

_num_map = zip((str(i) for i in range(0,10)),range(0,10))
_char_map = zip(string.ascii_uppercase,range(10,36))

# character map
CHAR_MAP = dict(chain(_num_map,_char_map))

# SEDOL character and weight map(no vowels)
SEDOL_CHAR_MAP = {k:v for (k,v) in CHAR_MAP.items() if k not in set(['A','E','I','O','U'])}

CUSIP_FIRST_CHAR = set((i for i,j in CINS_CODES))
CUSIP_FIRST_CHAR.update((str(i) for i in range(0,10)))

class SecurityId(metaclass=ABCMeta):
    """
    A financial security id that can be validated.

    Attributes:
        MIN_LEN : minimum length of security id with check digit.
        MAX_LEN : maximum length of security id with check digit.

    Note:
        "sid" input variable implies security id with check digit appended.
        "sid_" input variable implies security id w/o check digit.
    """

    MIN_LEN = 1
    MAX_LEN = None
    MAPPER = None

    def validate(self,sid):
        """ True if sid is valid security id, else raises IdError Exception."""

        if sid is None or sid is "" or (isinstance(sid,float) and isnan(sid)):
            raise NullError

        check_sum = self.calculate_checksum(sid[:(self.MAX_LEN - 1)])
        check_digit = val_check_digit(sid)

        if check_sum == check_digit:
            return True
        else:
            raise CheckSumError

    def is_valid(self,sid):
        """ True if sid is valid security id string, else False."""

        try:
            return self.validate(sid)
        except IdError:
            return False

    def calculate_checksum(self,sid):
        """ calculate the check digit."""

        self._id_check(sid)
        return self._calculate_checksum(sid)

    @abstractmethod
    def _calculate_checksum(self,sid):
        NotImplementedError

    def append_checksum(self,sid):
        """
        calculate and append check sum digit to security id.
        """

        sid += str(self.calculate_checksum(sid))
        return sid

    #def __str__(self):
    #    return "<security_id %s>" % self.__class__.__name__

    def _id_check(self,sid):
        if sid is None or sid is "" or (isinstance(sid,float) and isnan(sid)):
            raise NullError

        if not (self.MIN_LEN - 1) <= len(sid) <= (self.MAX_LEN - 1):
            raise LengthError

    def _iter_char(self,sid):
        try:
            return self.char2val(sid)
        except KeyError:
            raise CharacterError

    @abstractmethod
    def char2val(self,sid):
        NotImplementedError

class Sedol(SecurityId):
    """
    SEDOL identification number.

    Attributes:
        WEIGHTS : corresponding weighting for each character in SEDOL id
        _REV_WEIGHT : weighting from right to left charater removing the check digit
    """

    MAX_LEN = 7
    WEIGHTS = (1,3,1,7,3,9,1)
    _REV_WEIGHT = WEIGHTS[:-1][::-1]

    def _calculate_checksum(self,sid):
        sum_ = self._iter_char(sid)
        check_sum = (10 - sum_ % 10) % 10
        return check_sum

    def char2val(self,sid):
        return sum((SEDOL_CHAR_MAP[c]*w for (c,w) in zip(sid[::-1],self._REV_WEIGHT)))

class Cusip(SecurityId):
    """
    CUSIP identification number.

    References
    ----------
    https://www.cusip.com/pdf/CUSIP_Intro_03.14.11.pdf
    """

    MAX_LEN = 9

    def _calculate_checksum(self,sid):
        if sid[0] not in CUSIP_FIRST_CHAR:
            raise CountryCodeError

        vals = self._iter_char(sid)

        return _luhn_checksum(vals)

    def char2val(self,sid):
        return list((CHAR_MAP[c] for c in sid))

class Isin(SecurityId):
    """
    ISIN identification number.

    References
    ---------
    http://www.isin.org/education/
    https://en.wikipedia.org/wiki/International_Securities_Identification_Number
    """

    MIN_LEN = 12
    MAX_LEN = 12

    def _calculate_checksum(self,sid):
        # first two letters are two character ISO country code
        if sid[:2] not in COUNTRY_CODES:
            raise CountryCodeError

        vals = self._iter_char(sid)

        return _luhn_checksum(vals)

    def char2val(self,sid):
        return list(chain.from_iterable(_mydivmod(CHAR_MAP[c]) for c in sid))

def val_check_digit(sid):
    """ checks if check digit can convert to integer"""

    try:
        return int(sid[-1])
    except ValueError:
        raise CheckDigitError

def _luhn_checksum(vals):
    """ calculate the luhn check sum."""

    even = (x*2 for x in vals[::-2])
    odd_sum = luhn_sum(vals[-2::-2])
    even_sum = luhn_sum(even)
    sum_ = even_sum + odd_sum

    return (10 - sum_ % 10) % 10

def luhn_sum(vals):
    """ modular sum for luhn check sum."""

    return sum((x % 10 + (x // 10) for x in vals))

def _mydivmod(x):
     if x < 10:
         return (x,)
     else:
         return divmod(x,10)

class IdError(Exception): pass
class NullError(IdError): pass
class CheckDigitError(IdError): pass
class LengthError(IdError): pass
class CountryCodeError(IdError): pass
class CharacterError(IdError): pass
class CheckSumError(IdError): pass