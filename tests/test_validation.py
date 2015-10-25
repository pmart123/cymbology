
from unittest import TestCase
import pytest


from security_id import validation

from security_id.validation import NullError

xfail = pytest.mark.xfail


# empty exception tests
@pytest.mark.parametrize('obj',[
    pytest.mark.xfail(raises=NullError)((validation.Sedol())),
    pytest.mark.xfail(raises=NullError)((validation.Isin())),
    pytest.mark.xfail(raises=NullError)((validation.Cusip()))])
def test_none(obj):
    obj.validate(None)

@pytest.mark.parametrize('obj',[
    pytest.mark.xfail(raises=NullError)((validation.Sedol())),
    pytest.mark.xfail(raises=NullError)((validation.Isin())),
    pytest.mark.xfail(raises=NullError)((validation.Cusip()))])
def test_empty_string(obj):
    obj.validate("")

# SEDOL tests
@pytest.mark.parametrize('input',['0263494','2046251','0798059'])
def test_numeric_sedol(input):
    validation.Sedol().validate(input) == True

@pytest.mark.parametrize('input',['BCV7KT2',])
def test_char_sedol(input):
    validation.Sedol().validate(input) == True

@pytest.mark.parametrize('input',[
                            xfail('0263494567',raises=validation.LengthError),
                            xfail('BCV7KTM',raises=validation.CheckDigitError),
                            xfail('BCV7KT5',raises=validation.CheckSumError),
                            xfail(None,raises=validation.NullError)])
def test_sedol_failures(input):
    validation.Sedol().validate(input) == True

# ISIN tests
@pytest.mark.parametrize('input',['US0378331005','ES0109067019','GB0002374006','HK0941009539'])
def test_numeric_isin(input):
    validation.Isin().validate(input) == True

@pytest.mark.parametrize('input',['US30231G1022','CNE1000007Q1','US66987V1098'])
def test_char_isin(input):
    validation.Isin().validate(input) == True

@pytest.mark.parametrize('input',[
                            xfail('US03783310055',raises=validation.LengthError),
                            xfail('US037833100G',raises=validation.CheckDigitError),
                            xfail('XA0109067019',raises=validation.CountryCodeError),
                            xfail('US0378331009',raises=validation.CheckSumError)])
def test_isin_failures(input):
    validation.Isin().validate(input) == True


# CUSIP tests
@pytest.mark.parametrize('input',['037833100'])
def test_numeric_cusip(input):
    validation.Cusip().validate(input) == True

@pytest.mark.parametrize('input',['30303M102'])
def test_char_cusip(input):
    validation.Cusip().validate(input) == True

@pytest.mark.parametrize('input',[
                            xfail('30303M1024',raises=validation.LengthError),
                            xfail('30303M10#',raises=validation.CheckDigitError),
                            xfail('30303M102',raises=validation.CheckSumError)])
def test_cusip_failures(input):
    validation.Cusip().validate(input) == True
