import json

import pytest

from stockholm import Currency, Money, get_currency


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

    assert Money(1338, currency=Currency.SEK).keys() == ["value", "units", "nanos", "currency_code"]

    assert Money(1338, currency=Currency.SEK)["units"] == 1338
    assert Money(1338, currency=Currency.SEK)["value"] == "1338.00 SEK"

    with pytest.raises(KeyError):
        Money(1338, currency=Currency.SEK)["does_not_exist"]


def test_from_dict():
    input_dict = {"value": "13384711 JPY", "units": 13384711, "nanos": 0, "currency_code": "JPY"}
    assert str(Money.from_dict(input_dict)) == "13384711.00 JPY"
    assert str(Money.from_dict(input_dict).to_currency(get_currency(input_dict.get("currency_code")))) == "13384711 JPY"
    assert str(Money(input_dict)) == "13384711.00 JPY"
    assert str(Money(input_dict, currency=get_currency(input_dict.get("currency_code")))) == "13384711 JPY"


def test_from_json():
    input_value = '{"value": "13384711 JPY", "units": 13384711, "nanos": 0, "currency_code": "JPY"}'
    assert str(Money.from_json(input_value)) == "13384711.00 JPY"
    assert str(Money.from_json(input_value).to_currency(get_currency("JPY"))) == "13384711 JPY"
    assert str(Money.from_json(input_value).to_currency(get_currency("SEK"))) == "13384711.00 SEK"
    assert str(Money(input_value)) == "13384711.00 JPY"
    assert str(Money(input_value, currency=get_currency("JPY"))) == "13384711 JPY"


def test_from_protobuf():
    input_value = b"\n\x03USD\x10\x90\xf0\x84\x02\x18\x80\xbc\xe7\xd1\x01"
    assert str(Money.from_protobuf(input_value)) == "4274192.44 USD"
    assert str(Money.from_proto(input_value)) == "4274192.44 USD"
    assert str(Money.from_protobuf(input_value).to_currency("SEK")) == "4274192.44 SEK"
    assert str(Money(input_value)) == "4274192.44 USD"


def test_json():
    money = Money("-999999999999999999.999999999")
    json_string = json.dumps({"available": money.asdict()})

    str(Money(json.loads(json_string).get("available"))) == "-999999999999999999.999999999"
