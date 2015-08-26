 Feature: Validate the form of security id.
    In order to know a particular security id is valid.

    Background:
      Given the last character, called the check_digit, is a number.
      And a check_sum calculated from the remaining characters
      When the check_sum equals the check_digit
      Then a security is valid

    Given we have particular security id,
    When I check it's form
    Then I should see if the id is validate, or why it's not.

    Scenario: CUSIP
      Given a CUSIP with no check digit,
      When we want to calculate a check_sum,
      Then it should have eight characters, but leading zero characters can be omitted.
      And the first character should be a number, or a CINS country code character.
      And the Luhn algorithmn calculates its "check_sum".

   Scenario: ISIN
     Given a ISIN with no check digit,
     When we want to calculate a check_sum,
     Then it should have 11 characters.
     And the first two characters should be a ISO 3166-1 alpha-2 country code.
     And the Luhn mod N algorithmn calculates "check_sum".

   Scenario: SEDOL
     Given a non-check digit SEDOL id
     And weights (9, 3, 7, 1, 3, 1)
     When we want to calculate a check_sum,
     Then there should be six characters, but leading zero characters can be omitted.
     And it should contain 0-9 or ascii non-vowel characters.
     And we calculate the check_sum for SEDOL