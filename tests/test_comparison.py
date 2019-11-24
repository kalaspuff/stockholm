from typing import Any

import pytest

from stockholm import Money, CurrencyMismatchError


@pytest.mark.parametrize(
    "money, other, expected",
    [
        (Money("1"), Money("1"), True),
        (Money("0"), Money("0"), True),
        (Money("-0"), Money("0"), True),
        (Money("-0"), Money("-0"), True),
        (Money("-0", currency="SEK"), Money("-0"), True),
        (Money("-0 USD"), Money("SEK -0"), True),
        (Money("0 USD"), Money("SEK -0"), True),
        (Money("0"), Money("1"), False),
        (Money("-1"), Money("1"), False),
        (Money("-1"), Money("-1"), True),
        (Money("0", currency="SEK"), Money("0"), True),
        (Money("0", currency="SEK"), Money("0", currency="USD"), True),
        (Money("1", currency="SEK"), Money("1", currency="USD"), False),
        (Money("1", currency="SEK"), Money("1"), True),
        (Money(-1.5), Money("-1.50"), True),
        (Money(-1.5), "-1.5", True),
        (Money(-1.5), "-1.50000", True),
        (Money("-1.50000000"), "-1.50000 SEK", True),
        (Money(-1.5), "-1.50000 SEK", True),
        (Money(-1.5, currency="USD"), "-1.50000 SEK", False),
        (Money(4711, currency="EUR"), Money("4711.000000"), True),
        (Money(4711, currency="EUR"), 4711, True),
        (Money(4711, currency="EUR"), 1338, False),
        (Money(100, is_cents=True), 1, True),
        (Money(100, currency="SEK", is_cents=True), 1, True),
        (Money(1, currency="SEK", is_cents=True), 1, False),
        (Money(100, currency="SEK", is_cents=True), "1", True),
        (Money(1, currency="SEK", is_cents=True), 0.01, True),
        (Money(1, currency="SEK", is_cents=True), "0.01", True),
        (Money(100, currency="SEK", is_cents=True), "1.00", True),
        (Money(100, currency="SEK", is_cents=True), "1.00000", True),
        (Money(100, currency="SEK", is_cents=True), "1.0001", False),
        (Money(1, currency="SEK", is_cents=True), "1.0001", False),
        (Money(3.14), "3.1400", True),
        (Money(3.14), "3.1400 USD", True),
        (Money(3.14, currency="USD"), "3.1400 USD", True),
        (Money(3.14, currency="EUR"), "3.1400 USD", False),
        (Money("3.14", currency="EUR"), "3.1400", True),
        (Money("0"), 0, True),
        (Money("0"), 0.00, True),
        (Money("0"), 0.0000, True),
        (Money(0), 0, True),
        (Money("0.00000"), 0, True),
        (Money("0.00000"), "0 SEK", True),
        (Money("0.00000 SEK"), "0 SEK", True),
        (Money("0.00000", currency="SEK"), "0 SEK", True),
        (Money("0.00000", currency="USD"), "0 SEK", True),
        (Money("0.00000", currency="SEK"), "0 USD", True),
        (Money(0, currency="SEK"), "0 USD", True),
        (Money("0.00000", currency="SEK"), "0.00000 SEK", True),
        (Money("0.00000", currency="USD"), "0.00000 SEK", True),
        (Money("0.00001", currency="SEK"), "0.00001 SEK", True),
        (Money("0.00001", currency="USD"), "0.00001 SEK", False),
        (Money("1e5"), "100000", True),
        (Money("1e5"), "1e5", True),
        (Money("1e5", currency="SEK"), "1e5", True),
        (Money("1e6", currency="SEK"), "1e5", False),
        (Money("1e-2", currency="SEK"), Money(1, is_cents=True), True),
        (Money("-1e-2", currency="SEK"), -0.01, True),
        (Money("1", currency="SEK"), Money("1e2", is_cents=True), True),
        (Money(100, currency="SEK", is_cents=True), "SEK", False),
        (Money(100, currency="SEK", is_cents=True), "SEK SEK", False),
        (Money(100, currency="SEK", is_cents=True), "5,0 SEK", False),
        (Money(100, currency="SEK", is_cents=True), "500 ;;;", False),
        (Money(100, currency="SEK", is_cents=True), "1 USD", False),
    ],
)
def test_equal_comparison(money: Money, other: Any, expected: bool) -> None:
    result = bool(money == other)
    assert result is expected

    result = bool(money == str(other))
    assert result is expected

    result = bool(money != other)
    assert result is not expected


@pytest.mark.parametrize(
    "money, expected",
    [
        (Money(1), True),
        (Money(0), False),
        (Money("0.00"), False),
        (Money("0.01"), True),
        (Money(-1), True),
        (Money("-0.00"), False),
        (Money("-0.01"), True),
    ],
)
def test_falsy_truish(money, expected) -> None:
    assert bool(money) is expected


def test_compare_weights() -> None:
    assert Money(1) > Money(0)
    assert Money(4711) > Money(4710)
    assert Money(4711) >= Money(4710)
    assert Money(4710) >= Money(4710)
    assert Money(4710) <= Money(4710)
    assert not Money(4710) > Money(4710)
    assert not Money(4709) > Money(4710)
    assert Money(4709) < Money(4710)
    assert Money(4709) <= Money(4710)
    assert Money(0) >= Money(0)
    assert not Money(0) > Money(0)
    assert Money("3.14", currency="SEK") > Money(3)
    assert not Money("3.14", currency="SEK") > Money(3.14)
    assert Money("3.14", currency="SEK") >= Money(3.14)
    assert Money("3.14", currency="SEK") < Money(4)
    assert Money("3.14", currency="SEK") > Money(3, currency="SEK")
    assert Money("3.14", currency="SEK") < Money(4, currency="SEK")
    assert not Money("3.14", currency="SEK") > Money(3.14, currency="SEK")
    assert Money("3.14", currency="SEK") >= Money(3.14, currency="SEK")
    assert not Money(0) > 0
    assert not Money(-1) > 0
    assert Money(-1) < 0
    assert Money(-2) < -1
    assert Money(-2) >= -2
    assert not Money(-2) > -2
    assert not Money(-2.5) >= -2
    assert Money(-2) >= -3
    assert Money(-2) > -3
    assert not Money("-0") > 0
    assert not Money("-0") < 0
    assert not Money("-0.01") > 0
    assert Money("-0.01") < 0
    assert Money("31338", currency="USD") < 50000
    assert Money("31338", currency="USD") > 20000
    assert Money("31338", currency="USD") <= 31338
    assert Money("31338", currency="USD") >= 31338
    assert Money("31338", currency="USD") < "50000"
    assert Money("31338", currency="USD") > "20000"
    assert Money("31338", currency="USD") <= "31338"
    assert Money("31338", currency="USD") >= "31338"
    assert Money("31338", currency="USD") < "50000 USD"
    assert Money("31338", currency="USD") > "20000 USD"
    assert Money("31338", currency="USD") <= "31338 USD"
    assert Money("31338", currency="USD") >= "31338 USD"
    assert Money("31338", currency="USD") < "USD 50000"
    assert Money("31338", currency="USD") > "USD 20000"
    assert Money("31338", currency="USD") <= "USD 31338"
    assert Money("31338", currency="USD") >= "USD 31338"
    assert Money("31338.511115") < "50000 USD"
    assert Money("31338.511115") > "20000 USD"
    assert not Money("31338.511115") <= "31338 USD"
    assert Money("31338.000") <= "31338 USD"
    assert Money("31338.511115") >= "31338 USD"
    assert not (Money(10) / 3) == Money("3.333333333333")
    assert (Money(10) / 3) >= Money("3.333333333333")
    assert (Money(10) / 3) > Money("3.333333333333")
    assert Money(str(Money(10) / 3)) == Money(str(Money("3.333333333333")))
    assert Money(str(Money(10) / 3)) >= Money(str(Money("3.333333333333")))
    assert not Money(str(Money(10) / 3)) > Money(str(Money("3.333333333333")))


def test_compare_different_currencies() -> None:
    assert Money("0", currency="USD") == Money("0", currency="SEK")
    assert not Money("0", currency="USD") != Money("0", currency="SEK")
    assert Money("4711", currency="USD") != Money("4711", currency="SEK")
    assert not Money("4711", currency="USD") == Money("4711", currency="SEK")

    with pytest.raises(CurrencyMismatchError):
        Money("4711", currency="USD") >= Money("4711", currency="SEK")

    with pytest.raises(CurrencyMismatchError):
        Money("4711", currency="USD") > Money("4711", currency="SEK")

    with pytest.raises(CurrencyMismatchError):
        Money("4711", currency="USD") <= Money("4711", currency="SEK")

    with pytest.raises(CurrencyMismatchError):
        Money("4711", currency="USD") < Money("4711", currency="SEK")

    assert Money("4711", currency="USD") > "1338.00"
    assert Money("4711", currency="USD") >= "1338.00"
    assert Money("4711", currency="USD") > 1338
    assert Money("4711", currency="USD") >= 1338
    assert Money("4711") > "1338.00 SEK"
    assert Money("4711") >= "1338.00 SEK"
    assert Money("4711", currency="USD") > "1338.00 USD"
    assert Money("4711", currency="USD") >= "1338.00 USD"
    assert Money("4711 USD") > "1338.00 USD"
    assert Money("4711 USD") >= "1338.00 USD"
    with pytest.raises(CurrencyMismatchError):
        Money("4711", currency="USD") > "1338.00 SEK"
    with pytest.raises(CurrencyMismatchError):
        Money(0, currency="USD") > "1338.00 SEK"
    with pytest.raises(CurrencyMismatchError):
        Money(0, currency="USD") > "SEK 0"
    with pytest.raises(CurrencyMismatchError):
        Money("0.00 USD", currency="USD") > "1338.00 SEK"
    with pytest.raises(CurrencyMismatchError):
        Money("0.00 USD") > "SEK 0"

    assert min(Money("4711 SEK"), Money("1338 SEK")) == Money("1338 SEK")
    assert max(Money("4711.005"), Money("551 USD")) == Money("4711.005")

    assert Money(0) or Money(1) or Money(2) == Money(1)
    assert bool(Money(0) and Money(1)) is False
    assert bool(Money(2) and Money(1)) is True
