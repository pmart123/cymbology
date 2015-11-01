from unittest import TestCase

import pytest

from security_id.validation import Cusip, Isin, Sedol, val_check_digit
from security_id.exceptions import (CharacterError, CheckDigitError, CheckSumError,
                                    CountryCodeError, LengthError, NullError)


# --------------------------------------------------------------
# SecurityId tests
# --------------------------------------------------------------
class TestEmptyInput(TestCase):

    def setUp(self):
        self.validators = [Sedol(),Cusip(),Isin()]

    def test_none_input(self):
        # test None input
        for val in self.validators:
            with self.subTest(val=val):
                self.assertRaises(NullError,val.validate,None)

    def test_empty_string_input(self):
        for val in self.validators:
            with self.subTest(val=val):
                self.assertRaises(NullError,val.validate,"")

# @pytest.mark.parametrize('obj',[(Sedol()),(Isin()),(Cusip())])
# def test_empty_string(obj):
#     with pytest.raises(NullError):
#         obj.validate("")
#
#     with pytest.raises(NullError):
#         obj.validate(None)

class TestValid(TestCase):
    def setUp(self):
        self.validators = [Cusip()]
        self.validate_ids = ['30303M102']
        self.invalid_ids = ['30303M101']

    def test_valid(self):
        for val in zip(self.validators,self.validate_ids):
            with self.subTest(val=val):
                self.assertTrue(val[0].is_valid(val[1]))

# @pytest.mark.parametrize('obj,input,expected',
#                          [(Cusip(),'30303M102',True),
#                           (Cusip(),'30303M101',False)])
# def test_is_valid(obj,input,expected):
#     assert obj.is_valid(input) == expected

@pytest.mark.parametrize('obj,input,expected',
                         [(Cusip(),'03783310','037833100'),
                          (Cusip(),'3783310','37833100')])
def test_append_checksum(obj,input,expected):
    assert obj.append_checksum(input) == expected


@pytest.mark.parametrize('obj,input',
                         [(Sedol(),'0263494567'),(Isin(),'US03783310055'),
                           (Isin(),'US03'),(Cusip(),'30303M1024')])
def test_length_error(obj,input):
    with pytest.raises(LengthError):
        assert obj.validate(input)

@pytest.mark.parametrize('obj,input',
                         [(Sedol(),'20!6251'),(Isin(),'ES01@9067019'),(Cusip(),'03783*100')])
def test_character_error(obj,input):
    with pytest.raises(CharacterError):
        assert obj.validate(input)


@pytest.mark.parametrize('obj,input',
                         [(Sedol(),'BCV7KTM'),(Isin(),'US037833100G'),(Cusip(),'30303M10#')])
def test_checkdigit_error(obj,input):
    with pytest.raises(CheckDigitError):
        assert obj.validate(input)


@pytest.mark.parametrize('obj,input',
                         [(Sedol(),'BCV7KT5'),(Isin(),'US0378331009'),(Cusip(),'30303M103')])
def test_checksum_error(obj,input):
    with pytest.raises(CheckSumError):
        assert obj.validate(input)

# --------------------------------------------------------------
# SEDOL tests
# --------------------------------------------------------------

@pytest.mark.parametrize('input',['0263494','2046251','0798059'])
def test_numeric_sedol(input):
    assert Sedol().validate(input) == True

@pytest.mark.parametrize('input',['BCV7KT2'])
def test_char_sedol(input):
    assert Sedol().validate(input) == True

# --------------------------------------------------------------
# ISIN tests
# --------------------------------------------------------------

@pytest.mark.parametrize('input',['US0378331005','ES0109067019','GB0002374006','HK0941009539'])
def test_numeric_isin(input):
    assert Isin().validate(input) == True


@pytest.mark.parametrize('input',['US30231G1022','CNE1000007Q1','US66987V1098'])
def test_char_isin(input):
    assert Isin().validate(input) == True


def test_isin_country_code_error():
    with pytest.raises(CountryCodeError):
        Isin().validate('XA0109067019')


# --------------------------------------------------------------
# CUSIP tests
# --------------------------------------------------------------

@pytest.mark.parametrize('input',['037833100'])
def test_numeric_cusip(input):
    assert Cusip().validate(input) == True

@pytest.mark.parametrize('input',['30303M102'])
def test_char_cusip(input):
    assert Cusip().validate(input) == True

@pytest.mark.parametrize('input,expected',[('30303M102',True),('30303M101',False)])
def test_is_valid(input,expected):
    assert Cusip().is_valid(input) == expected

def test_cusip_country_code_error():
    with pytest.raises(CountryCodeError):
        Cusip().validate('I0303M109')

# --------------------------------------------------------------
# helper tests
# --------------------------------------------------------------

class TestValCheckDigit(TestCase):
    def test_val_check_digit(self):
        self.assertEqual(val_check_digit('abc1'),1)
        self.assertRaises(CheckDigitError,val_check_digit,'abc')