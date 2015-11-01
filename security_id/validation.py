import string
from abc import ABCMeta, abstractmethod
from itertools import chain
from math import isnan

from security_id.codes import CINS_CODES, COUNTRY_CODES
from security_id.exceptions import (IdError, NullError, LengthError, CountryCodeError,
                                    CharacterError, CheckSumError)
from security_id.helpers import val_check_digit, _luhnify

# character map
CHAR_MAP = dict(zip(string.digits + string.ascii_uppercase, range(0,36)))

# SEDOL character and weight map(no vowels)
SEDOL_CHAR_MAP = {k:v for (k,v) in CHAR_MAP.items() if k not in set('AEIOU')}

CUSIP_FIRST_CHAR = set(chain((c[0] for c in CINS_CODES), string.digits))

class SecurityId(metaclass=ABCMeta):
    """A financial security id that can be validated.

    Attributes
    ----------
    MIN_LEN : int
        minimum length of security id with check digit.
    MAX_LEN : int
        maximum length of security id with check digit.

    Notes
    -----
    "sid" input variable name implies security id with check digit appended.
    "sid_" input variable name implies security id w/o check digit.
    """

    MIN_LEN = 1
    MAX_LEN = None

    def validate(self, sid):
        """validate security id string.

        returns True if is validate id, else raises an IdError exception.

        """

        self._id_check(sid)

        check_sum = self.calculate_checksum(sid[:(self.MAX_LEN - 1)])
        check_digit = val_check_digit(sid)

        if check_sum == check_digit:
            return True
        else:
            raise CheckSumError

    def is_valid(self, sid):
        """True if sid is valid security id string, else False."""

        try:
            return self.validate(sid)
        except IdError:
            return False

    def calculate_checksum(self, sid_):
        """calculate the check digit."""

        self._id_check(sid_, offset=1)

        try:
            return self._calculate_checksum(sid_)
        except KeyError:
             raise CharacterError

    @abstractmethod
    def _calculate_checksum(self, sid_):
        NotImplementedError

    def append_checksum(self, sid_):
        """calculate and append check sum digit to security id."""

        sid_ += str(self.calculate_checksum(sid_))
        return sid_

    def __str__(self):
        return "<security_id %s>" % self.__class__.__name__

    def _id_check(self, sid_, offset=0):
        if sid_ is None or sid_ is "" or (isinstance(sid_, float) and isnan(sid_)):
            raise NullError

        if not (self.MIN_LEN - offset) <= len(sid_) <= (self.MAX_LEN - offset):
            raise LengthError

        self._additional_checks(sid_)

    def _additional_checks(self, sid_):
        pass


class Sedol(SecurityId):
    """SEDOL identification number.

    Attributes
    ----------
    WEIGHTS : tuple of int
        corresponding weighting for each character in SEDOL id
    _REV_WEIGHT : tuple of int
        weighting from right to left charater removing the check digit
    """

    MAX_LEN = 7
    WEIGHTS = (1,3,1,7,3,9,1)
    _REV_WEIGHT = WEIGHTS[:-1][::-1]

    def _calculate_checksum(self, sid_):
        sum_ = sum((SEDOL_CHAR_MAP[c]*w for (c, w) in zip(sid_[::-1], self._REV_WEIGHT)))
        check_sum = (10 - sum_ % 10) % 10
        return check_sum


class Cusip(SecurityId):
    """CUSIP identification number.

    References
    ----------
    https://www.cusip.com/pdf/CUSIP_Intro_03.14.11.pdf
    """

    MAX_LEN = 9

    def _calculate_checksum(self, sid_):
        return _luhnify((CHAR_MAP[c] for c in reversed(sid_)))

    def _additional_checks(self, sid_):
        if sid_[0] not in CUSIP_FIRST_CHAR:
            raise CountryCodeError


class Isin(SecurityId):
    """ISIN identification number.

    References
    ----------
    http://www.isin.org/education/
    https://en.wikipedia.org/wiki/International_Securities_Identification_Number
    """

    MIN_LEN = 12
    MAX_LEN = 12

    def _additional_checks(self, sid_):
        # first two letters are two character ISO country code
        if sid_[:2] not in COUNTRY_CODES:
            raise CountryCodeError

    def _calculate_checksum(self, sid_):
        return _luhnify(self._iter(sid_))

    def _iter(self, sid_):
        for c in reversed(sid_):
            val = CHAR_MAP[c]

            if val < 10:
                yield val
            else:
                yield from (val % 10, val // 10)
