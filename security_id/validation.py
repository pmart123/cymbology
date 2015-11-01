from abc import ABCMeta, abstractmethod
from math import isnan

from .exceptions import (IdError, NullError, LengthError,
                         CharacterError, CheckDigitError, CheckSumError)


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


def val_check_digit(sid):
    """checks if check digit can convert to integer"""

    try:
        return int(sid[-1])
    except ValueError:
        raise CheckDigitError