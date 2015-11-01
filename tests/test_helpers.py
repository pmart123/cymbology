from unittest import TestCase
import pytest
from security_id.exceptions import CheckDigitError
from security_id.helpers import luhn_modn_checksum, val_check_digit


@pytest.mark.parametrize('input,expected',[('0',0),('A',8)])
def test_luhn_modn_checksum(input,expected):
    assert luhn_modn_checksum(input) == expected


class TestValCheckDigit(TestCase):
    def test_val_check_digit(self):
        self.assertEqual(val_check_digit('abc1'),1)
        self.assertRaises(CheckDigitError,val_check_digit,'abc')