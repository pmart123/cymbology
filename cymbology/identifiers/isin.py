from cymbology.alphanum import CHAR_MAP
from cymbology.codes import COUNTRY_CODES
from cymbology.exceptions import CountryCodeError
from cymbology.luhn import _luhnify
from cymbology.validation import SecurityId


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
