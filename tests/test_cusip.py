from unittest import TestCase

from security_id import Cusip
from security_id.exceptions import CountryCodeError

from tests.test_alpha_numeric_id import AlphaNumericIdMixin


class TestCusip(AlphaNumericIdMixin, TestCase):
    length_issue = ['30303M1024']
    character_issue = ['03783*100']
    check_digit_issue = ['30303M10#']
    checksum_issue = ['30303M103']

    numeric_ids = ['037833100', '37833100']
    character_ids = ['30303M102']

    valid_id = '30303M102'
    invalid_id = ""

    checksum_param = {'sid_' : '03783310','sid': '037833100'}

    def setUp(self):
        self.obj = Cusip()

    def test_country_code_error(self):
        self.assertRaises(CountryCodeError, self.obj.validate, 'I0303M109')

    def tearDown(self):
        del self.obj