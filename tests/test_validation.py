
import pytest

from security_id.validation import Cusip, Isin, Sedol, val_check_digit, luhn_modn_checksum
from security_id.exceptions import CheckDigitError, CheckSumError, CountryCodeError, LengthError, NullError

xfail = pytest.mark.xfail

# class SecurityId shared methods

# empty exception tests
@pytest.mark.parametrize('obj',[
    pytest.mark.xfail(raises=NullError)((Sedol())),
    pytest.mark.xfail(raises=NullError)((Isin())),
    pytest.mark.xfail(raises=NullError)((Cusip()))])
def test_none(obj):
    obj.validate(None)

# empty string
@pytest.mark.parametrize('obj',[
    pytest.mark.xfail(raises=NullError)((Sedol())),
    pytest.mark.xfail(raises=NullError)((Isin())),
    pytest.mark.xfail(raises=NullError)((Cusip()))])
def test_empty_string(obj):
    obj.validate("")


# is_valid
@pytest.mark.parametrize('input,expected',
                         [('30303M102',True),
                          ('30303M101',False)])
def test_is_valid(input,expected):
    assert Cusip().is_valid(input) == expected

# appending checksum
@pytest.mark.parametrize('obj,input,expected',
                         [(Cusip(),'03783310','037833100'),
                          (Cusip(),'3783310','37833100')])
def test_append_checksum(obj,input,expected):
    assert obj.append_checksum(input) == expected


# length error
@pytest.mark.parametrize('obj,input',[
    pytest.mark.xfail(raises=LengthError)((Sedol(),'0263494567')),
    pytest.mark.xfail(raises=LengthError)((Isin(),'US03783310055')),
    pytest.mark.xfail(raises=LengthError)((Cusip(),'30303M1024'))])
def test_length_error(obj,input):
    obj.validate(input)

# checksum digit error
@pytest.mark.parametrize('obj,input',[
    pytest.mark.xfail(raises=CheckDigitError)((Sedol(),'BCV7KTM')),
    pytest.mark.xfail(raises=CheckDigitError)((Isin(),'US037833100G')),
    pytest.mark.xfail(raises=CheckDigitError)((Cusip(),'30303M10#'))])
def test_length_error(obj,input):
    obj.validate(input)



# SEDOL tests
@pytest.mark.parametrize('input',['0263494','2046251','0798059'])
def test_numeric_sedol(input):
    assert Sedol().validate(input) == True

@pytest.mark.parametrize('input',['BCV7KT2'])
def test_char_sedol(input):
    assert Sedol().validate(input) == True


@pytest.mark.parametrize('input',[
                            xfail('BCV7KT5',raises=CheckSumError)])
def test_sedol_failures(input):
    assert Sedol().validate(input) == True

# ISIN tests
@pytest.mark.parametrize('input',['US0378331005','ES0109067019','GB0002374006','HK0941009539'])
def test_numeric_isin(input):
    assert Isin().validate(input) == True

@pytest.mark.parametrize('input',['US30231G1022','CNE1000007Q1','US66987V1098'])
def test_char_isin(input):
    assert Isin().validate(input) == True

@pytest.mark.parametrize('input',[
                            xfail('XA0109067019',raises=CountryCodeError),
                            xfail('US0378331009',raises=CheckSumError)])
def test_isin_failures(input):
    assert Isin().validate(input) == True


# CUSIP tests
@pytest.mark.parametrize('input',['037833100'])
def test_numeric_cusip(input):
    assert Cusip().validate(input) == True

@pytest.mark.parametrize('input',['30303M102'])
def test_char_cusip(input):
    assert Cusip().validate(input) == True

@pytest.mark.parametrize('input',[
                            xfail('30303M102',raises=CheckSumError)])
def test_cusip_failures(input):
    assert Cusip().validate(input) == True

@pytest.mark.parametrize('input,expected',[('30303M102',True),('30303M101',False)])
def test_is_valid(input,expected):
    assert Cusip().is_valid(input) == expected

@pytest.mark.parametrize('input,expected',[('0',0),('A',8)])
def test_luhn_modn_checksum(input,expected):
    assert luhn_modn_checksum(input) == expected

def test_val_check_digit():
    assert val_check_digit('abc1') == 1

@xfail(raises=CheckDigitError)
def test_val_check_digit():
    assert val_check_digit('abc') == 1