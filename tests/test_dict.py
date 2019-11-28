from stockholm import Money, Currency, get_currency


def test_asdict():
    assert Money(1338, currency=Currency.SEK).asdict() == {
        "value": "1338.00 SEK",
        "units": 1338,
        "nanos": 0,
        "currency_code": "SEK",
    }
    assert Money("1338.4711", currency=Currency.SEK).as_dict() == {
        "value": "1338.4711 SEK",
        "units": 1338,
        "nanos": 471100000,
        "currency_code": "SEK",
    }
    assert dict(Money("0.123456", currency="SEK")) == {
        "value": "0.123456 SEK",
        "units": 0,
        "nanos": 123456000,
        "currency_code": "SEK",
    }
    assert dict(Money("0.1", currency=Currency("SEK"))) == {
        "value": "0.10 SEK",
        "units": 0,
        "nanos": 100000000,
        "currency_code": "SEK",
    }


def test_from_dict():
    d = {"value": "13384711 JPY", "units": 13384711, "nanos": 0, "currency_code": "JPY"}
    assert str(Money.from_dict(d)) == "13384711.00 JPY"
    assert str(Money.from_dict(d).to_currency(get_currency(d.get("currency_code")))) == "13384711 JPY"
    assert str(Money(d)) == "13384711.00 JPY"
    assert str(Money(d, currency=get_currency(d.get("currency_code")))) == "13384711 JPY"
