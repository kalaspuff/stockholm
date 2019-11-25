from decimal import Decimal
import pytest

from stockholm import Money, InvalidOperandError


def test_simple_addition() -> None:
    m1 = Money(0)
    assert isinstance(m1, Money)
    assert m1.amount == 0
    assert m1.currency is None
    assert str(m1) == "0.00"

    m2 = m1 + 1
    assert isinstance(m2, Money)
    assert m2.amount == 1
    assert m2.currency is None
    assert str(m2) == "1.00"

    m3 = m2 + "1.50 SEK"
    assert isinstance(m3, Money)
    assert m3.amount == 2.5
    assert m3.currency == "SEK"
    assert str(m3) == "2.50 SEK"


def test_one_line_addition() -> None:
    m = Money(0) + "1 EUR" + "2.5" + 1.51
    assert isinstance(m, Money)
    assert m.amount == Decimal("5.01")
    assert m.currency == "EUR"
    assert str(m) == "5.01 EUR"


def test_complex_addition() -> None:
    m = 1000 + 500 + Money(150, currency="NOK") + "4711.15000" + Money(-10000) + Money("55.70 NOK") + Decimal("25.01")
    assert isinstance(m, Money)
    assert m.amount == Decimal("-3558.14")
    assert m.currency == "NOK"
    assert str(m) == "-3558.14 NOK"


def test_simple_subtraction() -> None:
    m1 = Money("1000")
    assert isinstance(m1, Money)
    assert m1.amount == 1000
    assert m1.currency is None
    assert str(m1) == "1000.00"

    m2 = m1 - 1
    assert isinstance(m2, Money)
    assert m2.amount == 999
    assert m2.currency is None
    assert str(m2) == "999.00"

    m3 = m2 - "1500 SEK"
    assert isinstance(m3, Money)
    assert m3.amount == -501
    assert m3.currency == "SEK"
    assert str(m3) == "-501.00 SEK"

    m4 = "500" - m3
    assert isinstance(m4, Money)
    assert m4.amount == 1001
    assert m4.currency == "SEK"
    assert str(m4) == "1001.00 SEK"


def test_simple_multiplication() -> None:
    m1 = Money("333.3333", currency="SEK")
    assert isinstance(m1, Money)
    assert m1.amount == Decimal("333.3333")
    assert m1.currency == "SEK"
    assert str(m1) == "333.3333 SEK"

    m2 = m1 * 3
    assert isinstance(m2, Money)
    assert m2.amount == Decimal("999.9999")
    assert m2.currency == "SEK"
    assert str(m2) == "999.9999 SEK"

    m2 = 3 * m1
    assert isinstance(m2, Money)
    assert m2.amount == Decimal("999.9999")
    assert m2.currency == "SEK"
    assert str(m2) == "999.9999 SEK"

    m2 = m1 * Money(3)
    assert isinstance(m2, Money)
    assert m2.amount == Decimal("999.9999")
    assert m2.currency == "SEK"
    assert str(m2) == "999.9999 SEK"

    with pytest.raises(InvalidOperandError):
        m1 * m1


def test_simple_division() -> None:
    m1 = Money("21", currency="EUR")
    assert isinstance(m1, Money)
    assert m1.amount == 21
    assert m1.currency == "EUR"
    assert str(m1) == "21.00 EUR"

    m2 = m1 / 7
    assert isinstance(m2, Money)
    assert m2.amount == 3
    assert m2.currency == "EUR"
    assert str(m2) == "3.00 EUR"

    m3 = m1 / "7 EUR"
    assert isinstance(m3, Money)
    assert m3.amount == 3
    assert m3.currency is None
    assert str(m3) == "3.00"


def test_true_division() -> None:
    m1 = Money("100", currency="SEK")
    assert isinstance(m1, Money)
    assert m1.amount == 100
    assert m1.currency == "SEK"
    assert str(m1) == "100.00 SEK"

    m2 = m1 / 3
    assert isinstance(m2, Money)
    assert round(m2.amount, 9) == Decimal("33.333333333")
    assert m2.currency == "SEK"
    assert str(m2) == "33.333333333 SEK"

    with pytest.raises(ZeroDivisionError):
        m1 / 0

    m3 = Money("10.39", currency="USD")
    exchange_rate = m1 / m3
    assert isinstance(exchange_rate, Money)
    assert round(exchange_rate, 2) == Decimal("9.62")
    assert exchange_rate.currency is None
    assert str(exchange_rate) == "9.624639076"


def test_floor_division() -> None:
    m1 = Money("100", currency="SEK")
    assert isinstance(m1, Money)
    assert m1.amount == 100
    assert m1.currency == "SEK"
    assert str(m1) == "100.00 SEK"

    m2 = m1 // 3
    assert isinstance(m2, Money)
    assert m2.amount == 33
    assert m2.currency == "SEK"
    assert str(m2) == "33.00 SEK"

    m2 = m1 // "3 SEK"
    assert isinstance(m2, Money)
    assert m2.amount == 33
    assert m2.currency is None
    assert str(m2) == "33.00"

    with pytest.raises(ZeroDivisionError):
        m1 // 0

    m3 = Money("10.39", currency="USD")
    full_usd_amounts = m1 // m3
    assert isinstance(full_usd_amounts, Money)
    assert full_usd_amounts == 9
    assert full_usd_amounts.currency is None
    assert str(full_usd_amounts) == "9.00"


def test_modulus() -> None:
    m1 = Money("49", currency="SEK")
    assert isinstance(m1, Money)
    assert m1.amount == 49
    assert m1.currency == "SEK"
    assert str(m1) == "49.00 SEK"

    m2 = m1 % 14
    assert isinstance(m2, Money)
    assert m2.amount == 7
    assert m2.currency == "SEK"
    assert str(m2) == "7.00 SEK"

    m3 = m1 % Money(14, currency="USD")
    assert isinstance(m3, Money)
    assert m3.amount == 7
    assert m3.currency == "SEK"
    assert str(m3) == "7.00 SEK"

    m4 = m1 % Money(14, currency="SEK")
    assert isinstance(m3, Money)
    assert m4.amount == 7
    assert m4.currency == "SEK"
    assert str(m4) == "7.00 SEK"


def test_divmod() -> None:
    m1 = Money("49", currency="SEK")
    assert isinstance(m1, Money)
    assert m1.amount == 49
    assert m1.currency == "SEK"
    assert str(m1) == "49.00 SEK"

    m2, m3 = divmod(m1, 14)

    assert isinstance(m2, Money)
    assert m2.amount == 3
    assert m2.currency == "SEK"
    assert str(m2) == "3.00 SEK"

    assert isinstance(m3, Money)
    assert m3.amount == 7
    assert m3.currency == "SEK"
    assert str(m3) == "7.00 SEK"

    m3, m4 = divmod(m1, Money(14, currency="USD"))

    assert isinstance(m3, Money)
    assert m3.amount == 3
    assert m3.currency is None
    assert str(m3) == "3.00"

    assert isinstance(m4, Money)
    assert m4.amount == 7
    assert m4.currency == "SEK"
    assert str(m4) == "7.00 SEK"

    m5, m6 = divmod(m1, Money(14, currency="SEK"))

    assert isinstance(m5, Money)
    assert m5.amount == 3
    assert m5.currency is None
    assert str(m5) == "3.00"

    assert isinstance(m6, Money)
    assert m6.amount == 7
    assert m6.currency == "SEK"
    assert str(m6) == "7.00 SEK"


def test_pow() -> None:
    m1 = Money("2", currency="BIT")
    assert isinstance(m1, Money)
    assert m1.amount == 2
    assert m1.currency == "BIT"
    assert str(m1) == "2.00 BIT"

    m2 = m1 ** 4
    assert isinstance(m2, Money)
    assert m2.amount == 16
    assert m2.currency == "BIT"
    assert str(m2) == "16.00 BIT"

    m2 = m1 ** Money(4)
    assert isinstance(m2, Money)
    assert m2.amount == 16
    assert m2.currency == "BIT"
    assert str(m2) == "16.00 BIT"

    with pytest.raises(InvalidOperandError):
        m1 ** m1

    assert Money(2) ** Money(4) == 16


def test_bad_values() -> None:
    m = Money(1, currency="SEK")

    with pytest.raises(InvalidOperandError):
        m + "5,0"

    with pytest.raises(InvalidOperandError):
        m + "USD USD"

    with pytest.raises(InvalidOperandError):
        m - "50 000"


def test_object_arithmetics() -> None:
    m = Money(0, currency="SEK")
    assert m.add(1).add(2).add(3) == Money(6, currency="SEK")
    assert m.add(10).sub(5) == Money(5, currency="SEK")
    assert m.add(10).subtract(5) == Money(5, currency="SEK")

    with pytest.raises(Exception):
        assert m.add(1).add(2).add(3) == Money(6, currency="EUR")

    m2 = Money(471100, is_cents=True)
    assert m2.add(133800, is_cents=True) == Money(604900, is_cents=True)
    assert m2.add(133800, is_cents=True) == Money("6049.00")
