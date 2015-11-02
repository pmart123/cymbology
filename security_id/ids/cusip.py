from itertools import chain
import string
from security_id.alphanum import CHAR_MAP
from security_id.codes import CINS_CODES
from security_id.exceptions import CountryCodeError
from security_id.luhn import _luhnify
from security_id.validation import SecurityId


CUSIP_FIRST_CHAR = set(chain((c[0] for c in CINS_CODES), string.digits))

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