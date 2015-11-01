
from security_id.exceptions import (CharacterError, CheckDigitError, CheckSumError,
                                    LengthError, NullError)


class AlphaNumericIdTests(object):
    """

    error attribute class for SecurityId objects.

    """

    length_issue = None
    character_issue = None
    check_digit_issue = None
    checksum_issue = None

    numeric_ids = None
    character_ids = None

    # dictionary
    is_valid_ids = None
    check_digit_ids = None

    def __init__(self,
                 character_error,
                 checkdigit_error,
                 checksum_error,
                 length_error):
        pass

    def test_validate_none_input(self):
        self.assertRaises(NullError, self.obj.validate, None)

    def test_validate_empty_str_input(self):
        self.assertRaises(NullError, self.obj.validate, "")

    def test_length_error(self):
        for val in self.length_issue:
            with self.subTest(val=val):
                self.assertRaises(LengthError, self.obj.validate, val)

    def test_character_error(self):
        for val in self.character_issue:
            with self.subTest(val=val):
                self.assertRaises(CharacterError, self.obj.validate, val)

    def test_checkdigit_error(self):
        for val in self.check_digit_issue:
            with self.subTest(val=val):
                self.assertRaises(CheckDigitError, self.obj.validate, val)

    def test_checksum_error(self):
        for val in self.checksum_issue:
            with self.subTest(val=val):
                self.assertRaises(CheckSumError, self.obj.validate, val)

    def test_validate_numeric_id(self):
        for val in self.numeric_ids:
            with self.subTest(val=val):
                self.assertTrue(self.obj.validate(val))

    def test_validate_char_id(self):
        for val in self.character_ids:
            with self.subTest(val=val):
                self.assertTrue(self.obj.validate(val))

    def test_is_valid(self):
        self.assertTrue(self.obj.is_valid(self.valid_id))
        self.assertFalse(self.obj.is_valid(self.invalid_id))


    # TODO maybe dict?
    def test_append_checksum(self):
        self.assertEqual(self.obj.append_checksum(
                self.no_check_digit_id, self.check_digit))


