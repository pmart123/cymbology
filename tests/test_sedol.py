from unittest import TestCase

from cymbology import Sedol

from tests.test_alpha_numeric_id import AlphaNumericIdMixin


class TestSedol(AlphaNumericIdMixin, TestCase):
    length_issue = ['0263494567']
    character_issue = ['20!6251']
    check_digit_issue = ['BCV7KTM']
    checksum_issue = ['BCV7KT5']

    numeric_ids = ['0263494', '2046251', '0798059']
    character_ids = ['BCV7KT2']

    valid_id = '0263494'
    invalid_id = ""

    checksum_param = {'sid_': 'BCV7KT', 'sid': 'BCV7KT2'}

    def setUp(self):
        self.obj = Sedol()

    def tearDown(self):
        del self.obj
