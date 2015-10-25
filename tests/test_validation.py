
from unittest import TestCase

import pytest

from security_id.validation import Cusip, Isin, Sedol, val_check_digit, luhn_modn_checksum
from security_id.exceptions import CheckDigitError, CheckSumError, CountryCodeError, LengthError, NullError

xfail = pytest.mark.xfail


# --------------------------------------------------------------
# SecurityId tests
# --------------------------------------------------------------
class TestEmptyInput(TestCase):

    def test_none_input(self):
        # test None input
        self.assertRaises(NullError,Sedol().validate,None)
        self.assertRaises(NullError,Isin().validate,None)
        self.assertRaises(NullError,Cusip().validate,None)

    def test_empty_string(self):
        # test empty string input
        self.assertRaises(NullError,Sedol().validate,"")
        self.assertRaises(NullError,Isin().validate,"")
        self.assertRaises(NullError,Cusip().validate,"")

# empty string( or unittest case?)
# @pytest.mark.parametrize('obj',[(Sedol()),(Isin()),(Cusip())])
# def test_empty_string(obj):
#     with pytest.raises(NullError):
#         assert obj.validate("")


@pytest.mark.parametrize('input,expected',
                         [('30303M102',True),
                          ('30303M101',False)])
def test_is_valid(input,expected):
    assert Cusip().is_valid(input) == expected


@pytest.mark.parametrize('obj,input,expected',
                         [(Cusip(),'03783310','037833100'),
                          (Cusip(),'3783310','37833100')])
def test_append_checksum(obj,input,expected):
    assert obj.append_checksum(input) == expected


@pytest.mark.parametrize('obj,input',
                         [(Sedol(),'0263494567'),(Isin(),'US03783310055'),
                           (Isin(),'US03'),(Cusip(),'30303M1024')])
def test_length_error(obj,input):
    # check length error
    with pytest.raises(LengthError):
        assert obj.validate(input)


@pytest.mark.parametrize('obj,input',
                         [(Sedol(),'BCV7KTM'),(Isin(),'US037833100G'),(Cusip(),'30303M10#')])
def test_checkdigit_error(obj,input):
    # check digit error
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
    # country code failure
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

# --------------------------------------------------------------
# helper tests
# --------------------------------------------------------------
@pytest.mark.parametrize('input,expected',[('0',0),('A',8)])
def test_luhn_modn_checksum(input,expected):
    assert luhn_modn_checksum(input) == expected

class TestValCheckDigit(TestCase):
    def test_val_check_digit(self):
        self.assertEqual(val_check_digit('abc1'),1)
        self.assertRaises(CheckDigitError,val_check_digit,'abc')
