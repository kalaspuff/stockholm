from stockholm import Money


def test_basic_conversion():
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

    m3 = round(m1 / 3, 2)
    assert isinstance(m3, Money)
    assert m3 == Money("16.67", currency="USD")


def test_metadata_alive():
    m1 = Money(471100, currency="SEK", is_cents=True)
    m2 = Money(m1)
    assert m1.metadata == {"is_cents": True}
    assert m2.metadata == {"is_cents": True}
