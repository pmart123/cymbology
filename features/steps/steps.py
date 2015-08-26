from behave import given,when,then


from ... import security_id

@given(u'the last character, called the check_digit, is a number.')
def step_impl(context):
    assert security_id.validation.val_check_digit('3333')

@given(u'a check_sum calculated from the remaining characters')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a check_sum calculated from the remaining characters')

@when(u'the check_sum equals the check_digit')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the check_sum equals the check_digit')

@then(u'a security is valid')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then a security is valid')

@given(u'we have particular security id,')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given we have particular security id,')

@given(u'a CUSIP with no check digit,')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a CUSIP with no check digit,')

@when(u'we want to calculate a check_sum,')
def step_impl(context):
    raise NotImplementedError(u'STEP: When we want to calculate a check_sum,')

@then(u'it should have eight characters, but leading zero characters can be omitted.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then it should have eight characters, but leading zero characters can be omitted.')

@then(u'the first character should be a number, or a CINS country code character.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the first character should be a number, or a CINS country code character.')

@then(u'the Luhn algorithmn calculates its "check_sum".')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the Luhn algorithmn calculates its "check_sum".')

@given(u'a ISIN with no check digit,')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a ISIN with no check digit,')

@then(u'it should have 11 characters.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then it should have 11 characters.')

@then(u'the first two characters should be a ISO 3166-1 alpha-2 country code.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the first two characters should be a ISO 3166-1 alpha-2 country code.')

@then(u'the Luhn mod N algorithmn calculates "check_sum".')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the Luhn mod N algorithmn calculates "check_sum".')

@when(u'I check it\'s form')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I check it\'s form')

@then(u'I should see if the id is validate, or why it\'s not.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see if the id is validate, or why it\'s not.')

@given(u'a non-check digit SEDOL id')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a non-check digit SEDOL id')

@given(u'weights (9, 3, 7, 1, 3, 1)')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given weights (9, 3, 7, 1, 3, 1)')

@then(u'there should be six characters, but leading zero characters can be omitted.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then there should be six characters, but leading zero characters can be omitted.')

@then(u'it should contain 0-9 or ascii non-vowel characters.')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then it should contain 0-9 or ascii non-vowel characters.')

@then(u'we calculate the check_sum for SEDOL')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we calculate the check_sum for SEDOL')
