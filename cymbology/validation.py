from abc import ABCMeta, abstractmethod
from math import isnan

from cymbology.exceptions import (
    IdError, NullError, LengthError,
    InvalidCharacterError, CheckDigitError, CheckSumError
)


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

        returns sid if is validate, else raises an IdError exception.
        """

        null_check(sid)
        check_sum = self.calculate_checksum(sid[:-1])
        check_digit = val_check_digit(sid)

        if check_sum == check_digit:
            return sid
        else:
            message = 'The check sum, {}, does not equal the check digit {}'

            raise CheckSumError(message.format(check_sum, check_digit))

    def is_valid(self, sid):
        """True if sid is valid security id string, else False."""

        try:
            return bool(self.validate(sid))
        except IdError:
            return False

    def calculate_checksum(self, sid_):
        """calculate the check digit."""

        self._id_check(sid_, offset=1)

        try:
            return self._calculate_checksum(sid_)
        except KeyError:
            raise InvalidCharacterError(
                '{} identifier contains invalid characters'.format(
                    self.__class__.__qualname__
                )
            )

    @abstractmethod
    def _calculate_checksum(self, sid_):
        NotImplementedError

    def append_checksum(self, sid_):
        """calculate and append check sum digit to security id."""

        sid_ += str(self.calculate_checksum(sid_))
        return sid_

    def __str__(self):
        return "<cymbology %s>" % self.__class__.__name__

    def _id_check(self, sid_, offset=0):

        null_check(sid_)

        if not (self.MIN_LEN - offset) <= len(sid_) <= (self.MAX_LEN - offset):
            raise LengthError(
                length_error_message(
                    self.__class__.__qualname__, self.MIN_LEN, self.MAX_LEN
                )
            )

        self._additional_checks(sid_)

    def _additional_checks(self, sid_):
        pass


def null_check(sid):
    """Check if id string is null."""

    if not sid or (isinstance(sid, float) and isnan(sid)):
        raise NullError


def val_check_digit(sid):
    """checks if check digit can convert to integer."""

    try:
        return int(sid[-1])
    except ValueError:
        raise CheckDigitError(
            "The identifier's check digit must be an integer."
        )


def length_error_message(identifier, min_length=None, max_length=None):
    """Build length error message."""

    additional = []

    if min_length:
        additional.append('at least length {}'.format(min_length))

    if max_length:
        additional.append('at most length {}'.format(max_length))

    body = ', '.join(additional)
    message = '{} identifier input must {}.'.format(identifier, body)

    return message
