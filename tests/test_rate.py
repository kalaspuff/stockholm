import json

import pytest

import stockholm
from stockholm import ConversionError, ExchangeRate, Money, Rate


def test_rate():
    assert Rate(100) == 100
    assert Rate("100.50551") == ExchangeRate("100.50551")
    assert str(Rate("4711.1338")) == "4711.1338"

    assert Rate(100).currency is None
    assert Rate(100).currency_code is None
    assert Rate(100).amount == 100
    assert Rate(100).value == "100.00"

    assert Rate(50) < 51
    assert Rate(50) > 49
    assert Rate(50) > Rate(49)

    assert Rate(50) + Rate(50) == 100
    assert (Rate(50) + Rate(50)).__class__ is Rate
    assert str(Rate(50) + Rate(50)) == "100.00"
    assert repr(Rate(50) + Rate(50)) == '<stockholm.Rate: "100.00">'

    assert (Rate(50) + Rate(50) + Money(50)).__class__ is Money
    assert str(Rate(50) + Rate(50) + Money(50)) == "150.00"
    assert repr(Rate(50) + Rate(50) + Money(50)) == '<stockholm.Money: "150.00">'

    assert Rate(Money(100)) == Rate(100)
    assert Rate(Money(100)).__class__ is Rate


def test_bad_rates():
    with pytest.raises(ConversionError):
        Rate(1, currency="EUR")

    with pytest.raises(ConversionError):
        Rate(Money(1, currency="SEK"))

    with pytest.raises(ConversionError):
        Rate(100, from_sub_units=True)

    with pytest.raises(ConversionError):
        Rate(1).to_currency("SEK")

    with pytest.raises(ConversionError):
        Rate(1).to_sub_units()

    with pytest.raises(ConversionError):
        Rate(1).sub_units


def test_rate_hashable() -> None:
    m = stockholm.Rate(0)
    assert hash(m)


def test_rate_asdict():
    assert Rate(1338).asdict() == {
        "value": "1338.00",
        "units": 1338,
        "nanos": 0,
    }
    assert Rate("1338.4711").as_dict() == {
        "value": "1338.4711",
        "units": 1338,
        "nanos": 471100000,
    }
    assert dict(Rate("0.123456")) == {
        "value": "0.123456",
        "units": 0,
        "nanos": 123456000,
    }
    assert dict(Rate("0.1")) == {
        "value": "0.10",
        "units": 0,
        "nanos": 100000000,
    }

    assert Rate(1338).keys() == ["value", "units", "nanos"]

    assert Rate(1338)["units"] == 1338
    assert Rate(1338)["value"] == "1338.00"

    with pytest.raises(KeyError):
        Rate(1338)["does_not_exist"]


def test_rate_from_dict():
    d = {"value": "13384711", "units": 13384711, "nanos": 0}
    assert str(Rate.from_dict(d)) == "13384711.00"
    assert str(Rate(d)) == "13384711.00"


def test_rate_json():
    rate = Rate("-999999999999999999.999999999")
    json_string = json.dumps({"rate": rate.asdict()})

    str(Rate(json.loads(json_string).get("rate"))) == "-999999999999999999.999999999"
