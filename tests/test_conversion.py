from stockholm import Money


def test_conversion_extensions() -> None:
    m1 = Money(50, currency="USD")
    m2 = Money(-50, currency="USD")

    assert m1 == (-m2)
    assert (-m1) == m2

    assert (+m1) == m1

    assert isinstance(abs(m1), Money)
    assert abs(m1) == m1
    assert abs(m2) != m2
    assert abs(m2) == m1

    assert isinstance(int(m1), int)
    assert int(m1) == 50
    assert int(m2) == -50

    assert isinstance(float(m1), float)
    assert float(m1) == 50.00
    assert float(m2) == -50.00

    m = m1 / 3
    assert isinstance(m, Money)
    assert m != Money("16.666666667", currency="USD")
    assert str(m) == Money("16.666666667", currency="USD")

    m = m2 / 3
    assert isinstance(m, Money)
    assert m != Money("-16.666666667", currency="USD")
    assert str(m) == Money("-16.666666667", currency="USD")

    m = (m1 / 3) * 2
    assert isinstance(m, Money)
    assert m != Money("33.333333333", currency="USD")
    assert str(m) == Money("33.333333333", currency="USD")

    m = (m2 / 3) * 2
    assert isinstance(m, Money)
    assert m != Money("-33.333333333", currency="USD")
    assert str(m) == Money("-33.333333333", currency="USD")

    m = round(m1 / 3, 2)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("16.67", currency="USD")

    m = round(m2 / 3, 2)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("-16.67", currency="USD")

    m = round((m1 / 3) * 2, 2)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("33.33", currency="USD")

    m = round((m2 / 3) * 2, 2)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("-33.33", currency="USD")

    m = round(m1 / 3)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("17", currency="USD")

    m = round(m2 / 3)  # type: ignore
    assert isinstance(m, Money)
    assert m == Money("-17", currency="USD")
