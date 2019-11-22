from decimal import Decimal

from stockholm import Money


def test_simple_addition():
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


def test_one_line_addition():
    m = Money(0) + "1 EUR" + "2.5" + 1.51
    assert isinstance(m, Money)
    assert m.amount == Decimal("5.01")
    assert m.currency == "EUR"
    assert str(m) == "5.01 EUR"


def test_complex_addition():
    m = 1000 + 500 + Money(150, currency="NOK") + "4711.15000" + Money(-10000) + Money("55.70 NOK") + Decimal("25.01")
    assert isinstance(m, Money)
    assert m.amount == Decimal("-3558.14")
    assert m.currency == "NOK"
    assert str(m) == "-3558.14 NOK"


def test_simple_subtraction():
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


def test_simple_multiplication():
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


def test_simple_division():
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
    assert isinstance(m3, Decimal)
    assert m3 == 3
    assert str(m3) == "3"


def test_true_division():
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


def test_floor_division():
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


def test_modulus():
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


def test_divmod():
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


def test_pow():
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
