from stockholm import Currency, Money


def test_currency():
    EUR = Currency("EUR")
    assert str(EUR) == "EUR"

    m = Money(100, EUR)
    assert str(m) == "100.00 EUR"
    assert isinstance(m.currency, Currency)
    assert str(m.currency) == "EUR"
    assert str(m.currency.ticker) == "EUR"

def test_currency_arithmetics():
    EUR = Currency("EUR")
    SEK = Currency("SEK")
    assert EUR
    assert EUR == "EUR"
    assert EUR != "SEK"
    assert EUR != SEK

    m1 = Money(100, EUR)
    m2 = Money(100, "EUR")
    assert m1 == m2

    m3 = Money(100, "SEK")
    assert m1 != m3

    m4 = Money(100, SEK)
    assert m1 != m4
    assert m3 == m4