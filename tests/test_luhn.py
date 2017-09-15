import pytest

from cymbology.luhn import luhn_modn_checksum


@pytest.mark.parametrize('input,expected',[('0',0),('A',8)])
def test_luhn_modn_checksum(input,expected):
    assert luhn_modn_checksum(input) == expected
