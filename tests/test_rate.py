import json

import pytest

import stockholm
from stockholm import ConversionError, ExchangeRate, Money, Number, Rate


def test_rate() -> None:
    assert Rate(100) == 100
    assert Rate("100.50551") == ExchangeRate("100.50551")
    assert str(Rate("4711.1338")) == "4711.1338"

    assert Rate(100).currency is None
    assert Rate(100).currency_code is None
    assert Rate(100).amount == 100
    assert Rate(100).value == "100"

    assert Rate(100.5).amount == 100.5
    assert Rate(100.5).value == "100.5"
    assert Rate(100.50).value == "100.5"
    assert Rate(100.42).value == "100.42"

    assert Rate(50) < 51
    assert Rate(50) > 49
    assert Rate(50) > Rate(49)

    assert Rate(50) + Rate(50) == 100
    assert (Rate(50) + Rate(50)).__class__ is Rate
    assert str(Rate(50) + Rate(50)) == "100"
    assert repr(Rate(50) + Rate(50)) == '<stockholm.Rate: "100">'

    assert (Rate(50) + Rate(50) + Money(50)).__class__ is Money
    assert str(Rate(50) + Rate(50) + Money(50)) == "150.00"
    assert repr(Rate(50) + Rate(50) + Money(50)) == '<stockholm.Money: "150.00">'

    assert Rate(Money(100)) == Rate(100)
    assert Rate(Money(100)).__class__ is Rate


def test_number() -> None:
    assert Number(100) == 100
    assert Number("100.50551") == 100.50551
    assert str(Number("4711.1338")) == "4711.1338"

    assert Number(100.50).value == "100.5"
    assert Number(100.42).value == "100.42"
    assert Number(nanos=10).value == "0.00000001"

    assert repr(Number(0.00001) + Number(53.5)) == '<stockholm.Number: "53.50001">'
    assert (Number(0.00001) + Number(53.5)).asdict() == {"nanos": 500010000, "units": 53, "value": "53.50001"}

    assert str(Number(1.5).to_currency("USD")) == "1.50 USD"

    assert Number(Money(100)).__class__ is Number


def test_bad_rates() -> None:
    with pytest.raises(ConversionError):
        Rate(1, currency="EUR")

    with pytest.raises(ConversionError):
        Rate(Money(1, currency="SEK"))

    with pytest.raises(ConversionError):
        Rate(100, from_sub_units=True)

    with pytest.raises(ConversionError):
        Rate.from_sub_units(100)

    with pytest.raises(ConversionError):
        Rate(1).to_sub_units()

    with pytest.raises(ConversionError):
        Rate(1).sub_units


def test_rate_hashable() -> None:
    r1 = stockholm.Rate(0)
    r2 = stockholm.Rate(0)
    r3 = stockholm.Rate(1)
    n = stockholm.Number(0)

    assert hash(r1)
    assert hash(r1) == hash(r2)
    assert hash(r1) != hash(r3)
    assert hash(r1) != hash(n)


def test_rate_asdict() -> None:
    assert Rate(1338).asdict() == {
        "value": "1338",
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
        "value": "0.1",
        "units": 0,
        "nanos": 100000000,
    }

    assert Rate(1338).keys() == ["value", "units", "nanos"]

    assert Rate(1338)["units"] == 1338
    assert Rate(1338)["value"] == "1338"

    with pytest.raises(KeyError):
        Rate(1338)["does_not_exist"]


def test_asdict_with_keys() -> None:
    assert Rate(1338).asdict(keys=("value", "amount")) == {
        "value": "1338",
        "amount": "1338",
    }
    assert Rate("1338.4711").as_dict(keys=("value", "amount")) == {
        "value": "1338.4711",
        "amount": "1338.4711",
    }


def test_rate_from_dict() -> None:
    d = {"value": "13384711", "units": 13384711, "nanos": 0}
    assert str(Rate.from_dict(d)) == "13384711"
    assert str(Rate(d)) == "13384711"

    d = {"units": 5, "nanos": 100000}
    assert str(Rate.from_dict(d)) == "5.0001"
    assert str(Rate(d)) == "5.0001"


def test_rate_json() -> None:
    rate = Rate("-999999999999999999.999999999")
    json_string = json.dumps({"rate": rate.asdict()})
    assert str(Rate(json.loads(json_string).get("rate"))) == "-999999999999999999.999999999"

    assert (
        Rate({"units": 5, "nanos": 100000}).as_json()
        == Rate({"units": 5, "nanos": 100000}).json()
        == '{"value": "5.0001", "units": 5, "nanos": 100000}'
    )

    assert str(Rate(Rate({"amount": "13.095"}).as_json())) == "13.095"
    assert str(Rate(Rate({"units": 13, "nanos": 95000000}).as_json())) == "13.095"
    assert str(Rate(Rate({"nanos": 10}).as_json())) == "0.00000001"
