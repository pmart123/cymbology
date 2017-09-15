from types import MappingProxyType

from cymbology.alphanum import CHAR_MAP
from cymbology.validation import SecurityId


# SEDOL character and weight map(no vowels)
SEDOL_CHAR_MAP = MappingProxyType(
    {k: v for (k, v) in CHAR_MAP.items() if k not in set('AEIOU')}
)


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
    WEIGHTS = (1, 3, 1, 7, 3, 9, 1)
    _REV_WEIGHT = WEIGHTS[:-1][::-1]

    def _calculate_checksum(self, sid_):
        sum_ = sum((SEDOL_CHAR_MAP[c] * w
                    for (c, w) in zip(sid_[::-1], self._REV_WEIGHT)))
        check_sum = (10 - sum_ % 10) % 10

        return check_sum
