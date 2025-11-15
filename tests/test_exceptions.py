import pureyak


def test_invalid_choice_error():
    x = 0
    choices = [1, 2, 3]
    error = pureyak.exceptions.InvalidChoiceError(x, choices)
    actual = error.message
    expected = "value=0 invalid choice - expected a value from (1, 2, 3)"
    assert actual == expected
