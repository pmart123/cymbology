from cymbology.exceptions import (CharacterError, CheckDigitError, CheckSumError,
                                  LengthError, NullError)


class AlphaNumericIdMixin(object):
    """mixin class for alpha numeric security ids."""

    length_issue = None
    character_issue = None
    check_digit_issue = None
    checksum_issue = None

    numeric_ids = None
    character_ids = None

    valid_id = None
    invalid_id = None

    # dictionary
    checksum_param = None

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
                self.assertEqual(self.obj.validate(val), val)

    def test_validate_char_id(self):
        for val in self.character_ids:
            with self.subTest(val=val):
                self.assertTrue(self.obj.validate(val))

    def test_is_valid(self):
        self.assertTrue(self.obj.is_valid(self.valid_id))
        self.assertFalse(self.obj.is_valid(self.invalid_id))

    def test_append_checksum(self):
        self.assertEqual(self.obj.append_checksum(
            self.checksum_param['sid_']),self.checksum_param['sid'])

    def test_calculate_checksum(self):
        self.assertEqual(self.obj.calculate_checksum(
            self.checksum_param['sid_']), int(self.checksum_param['sid'][-1]))
