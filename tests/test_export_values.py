from decimal import Decimal
from typing import Any

import pytest

from stockholm import Money, MoneyProtoMessage


@pytest.mark.parametrize(
    "value, expected_units, expected_nanos, expected_string",
    [
        ("3712381.75", 3712381, 750000000, "3712381.75"),
        ("-1.75", -1, -750000000, "-1.75"),
        ("0", 0, 0, "0.00"),
        ("0.000000001", 0, 1, "0.000000001"),
        ("0.000001", 0, 1000, "0.000001"),
        ("-0.000001", 0, -1000, "-0.000001"),
        (4711.50, 4711, 500000000, "4711.50"),
        ("-0.00", 0, 0, "0.00"),
        ("0.0000000001", 0, 0, "0.00"),
        ("3.141592650", 3, 141592650, "3.14159265"),
        ("3.141592653", 3, 141592653, "3.141592653"),
        ("3.1415926535", 3, 141592654, "3.141592654"),
        ("3.1415926530", 3, 141592653, "3.141592653"),
        ("3.14159265305", 3, 141592653, "3.141592653"),
        ("3.14159265349", 3, 141592653, "3.141592653"),
        ("3.1415926534999", 3, 141592653, "3.141592653"),
        ("3.14159265349990", 3, 141592653, "3.141592653"),
        ("3.14159265349995", 3, 141592653, "3.141592653"),
        ("3.14159265349999", 3, 141592653, "3.141592653"),
        ("3.1415926535000000", 3, 141592654, "3.141592654"),
        ("-3.1415926535000000", -3, -141592654, "-3.141592654"),
        ("999999999999999999.999999999", 999999999999999999, 999999999, "999999999999999999.999999999"),
        ("999999999999999999.999999998", 999999999999999999, 999999998, "999999999999999999.999999998"),
        ("999999999999999999.9999999985", 999999999999999999, 999999999, "999999999999999999.999999999"),
        ("-999999999999999999.999999999", -999999999999999999, -999999999, "-999999999999999999.999999999"),
        ("1.999999999", 1, 999999999, "1.999999999"),
        ("1.99999999949", 1, 999999999, "1.999999999"),
        ("1.99999999949999", 1, 999999999, "1.999999999"),
        ("1.9999999999", 2, 0, "2.00"),
        ("0.00000000049990", 0, 0, "0.00"),
        ("0.000000000499999999", 0, 0, "0.00"),
        ("0.000000000500000000", 0, 1, "0.000000001"),
        ("0.00000000099999", 0, 1, "0.000000001"),
        ("-1.999999999", -1, -999999999, "-1.999999999"),
        ("-1.99999999949", -1, -999999999, "-1.999999999"),
        ("-1.99999999949999", -1, -999999999, "-1.999999999"),
        ("-1.9999999999", -2, 0, "-2.00"),
        ("-0.00000000049999", 0, 0, "0.00"),
        ("-0.00000000099999", 0, -1, "-0.000000001"),
    ],
)
def test_value_tuple(value: Any, expected_units: int, expected_nanos: int, expected_string: str) -> None:
    m = Money(value)
    assert m.units == expected_units
    assert m.nanos == expected_nanos
    assert m.amount_as_string() == expected_string


def test_info_methods() -> None:
    m = Money("4711.75", currency="EUR")

    assert m.amount == Decimal("4711.75")
    assert m.currency == "EUR"
    assert m.currency_code == "EUR"
    assert m.units == 4711
    assert m.nanos == 750000000

    assert m.amount_as_string() == "4711.75"
    assert m.amount_as_string(min_decimals=5, max_decimals=8) == "4711.75000"
    assert m.amount_as_string(min_decimals=0, max_decimals=8) == "4711.75"
    assert m.amount_as_string(min_decimals=0, max_decimals=1) == "4711.8"
    assert m.amount_as_string(min_decimals=0, max_decimals=0) == "4712"
    assert m.amount_as_string(max_decimals=0) == "4712"
    assert m.amount_as_string(min_decimals=10) == "4711.7500000000"

    with pytest.raises(ValueError):
        m.amount_as_string(min_decimals=2, max_decimals=0)

    assert m.as_string() == "4711.75 EUR"
    assert m.as_str() == "4711.75 EUR"
    assert m.as_decimal() == Decimal("4711.75")
    assert m.as_int() == 4711
    assert m.as_float() == float(m)
    assert m.is_zero() is False
    assert m.is_signed() is False

    assert m.as_json() == '{"value": "4711.75 EUR", "units": 4711, "nanos": 750000000, "currency_code": "EUR"}'
    assert m.json() == '{"value": "4711.75 EUR", "units": 4711, "nanos": 750000000, "currency_code": "EUR"}'

    assert type(m.as_protobuf()) is MoneyProtoMessage
    assert m.as_protobuf().currency_code == "EUR"
    assert m.as_protobuf().units == 4711
    assert m.as_protobuf().nanos == 750000000
    assert m.as_protobuf().SerializeToString() == b"\n\x03EUR\x10\xe7$\x18\x80\xaf\xd0\xe5\x02"
    assert m.as_proto().SerializeToString() == b"\n\x03EUR\x10\xe7$\x18\x80\xaf\xd0\xe5\x02"
    assert m.protobuf().SerializeToString() == b"\n\x03EUR\x10\xe7$\x18\x80\xaf\xd0\xe5\x02"
    assert m.proto().SerializeToString() == b"\n\x03EUR\x10\xe7$\x18\x80\xaf\xd0\xe5\x02"

    assert type(m.as_protobuf(proto_class=MoneyProtoMessage)) is MoneyProtoMessage

    with pytest.raises(TypeError):
        m.as_protobuf(proto_class=None)

    assert Money(0).is_zero() is True
    assert Money(0).is_signed() is False

    assert Money(-1).is_signed() is True

    m = Money("-0.0000000001", currency="EUR")

    assert m.amount == Decimal("-0.0000000001")
    assert m.currency == "EUR"
    assert m.units == 0
    assert m.nanos == 0

    assert m.amount_as_string() == "0.00"
    assert m.amount_as_string(max_decimals=10) == "-0.0000000001"
    assert m.as_string() == "0.00 EUR"
    assert m.as_decimal() == Decimal("-0.0000000001")
    assert m.as_int() == 0
    assert m.is_zero() is False
    assert m.is_signed() is True
