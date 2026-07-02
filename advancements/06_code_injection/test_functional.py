"""Functional tests -- the calculator evaluates arithmetic correctly."""


def test_addition_and_precedence(mod):
    assert mod.calculate("2 + 3 * 4") == 14


def test_parentheses(mod):
    assert mod.calculate("(1 + 2) * 3") == 9


def test_division(mod):
    assert mod.calculate("10 / 4") == 2.5
