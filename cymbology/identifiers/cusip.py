from itertools import chain
import string
from cymbology.alphanum import CHAR_MAP
from cymbology.codes import CINS_CODES
from cymbology.exceptions import CountryCodeError
from cymbology.luhn import _luhnify
from cymbology.validation import SecurityId


CUSIP_FIRST_CHAR = frozenset(chain((c[0] for c in CINS_CODES), string.digits))


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


def cusip_from_isin(isin):
    """Convert ISIN security identifiers to CUSIP identifiers."""

    if not isin.startswith('US'):
        raise CountryCodeError

    return Cusip().validate(isin[2:-1])
