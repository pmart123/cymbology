from unittest import TestCase

from cymbology import Isin
from cymbology.exceptions import CountryCodeError

from tests.test_alpha_numeric_id import AlphaNumericIdMixin


class TestIsin(AlphaNumericIdMixin, TestCase):
    length_issue = ['US03783310055']
    character_issue = ['ES01@9067019']
    check_digit_issue = ['US037833100G']
    checksum_issue = ['US0378331009']

    numeric_ids = ['US0378331005', 'ES0109067019', 'GB0002374006', 'HK0941009539']
    character_ids = ['US30231G1022', 'CNE1000007Q1', 'US66987V1098']

    valid_id = 'CNE1000007Q1'
    invalid_id = ""

    checksum_param = {'sid_': 'ES010906701', 'sid': 'ES0109067019'}

    def setUp(self):
        self.obj = Isin()

    def test_country_code_error(self):
        self.assertRaises(CountryCodeError, self.obj.validate, 'XA0109067019')

    def tearDown(self):
        del self.obj
