from decimal import Decimal
from typing import Any, Optional

import pytest

from stockholm import ConversionError, Currency, Money, MoneyProtoMessage


@pytest.mark.parametrize(
    "amount, currency, exception_expected",
    [
        (1, None, None),
        ("1", None, None),
        ("1.00", None, None),
        (10000000000, None, None),
        (100000000000000, None, None),
        (1.15, None, None),
        ("1.15", None, None),
        ("1.1500", None, None),
        ("1.15.00", None, ConversionError),
        ("1338.31337", None, None),
        ("+1338.31337", None, None),
        ("-1338.31337", None, None),
        ("--1338.31337", None, ConversionError),
        ("1338..31337", None, ConversionError),
        ("1338.", None, None),
        ("", None, ConversionError),
        ("  ", None, ConversionError),
        ("10  ", None, None),
        ("-0.00", None, None),
        ("-0.01", None, None),
        ("-.00", None, None),
        ("-.01", None, None),
        ("-00", None, None),
        ("-01", None, None),
        ("00009", None, None),
        (".001", None, None),
        ("-.001", None, None),
        ("-.0", None, None),
        (".0", None, None),
        ("..0", None, ConversionError),
        ("3.", None, None),
        ("-3.", None, None),
        (".", None, ConversionError),
        ("SEK", None, ConversionError),
        ("-SEK", None, ConversionError),
        ("-0SEK", None, ConversionError),
        ("SEK0", None, ConversionError),
        ("SEK-0", None, ConversionError),
        ("SEK-0", None, ConversionError),
        ("SEK 0", None, None),
        ("SEK 4711.15", None, None),
        ("0 USD", None, None),
        ("4711.15 USD", None, None),
        ("SEK 0 USD", None, ConversionError),
        ("SEK 4711.15 USD", None, ConversionError),
        (":SEK 0.00", None, ConversionError),
        ("1000.4141561 XDR", None, None),
        ("1e5", None, None),
        ("-1e2", None, None),
        ("-1e-2", None, None),
        ("1000 SEK", None, None),
        ("1000 SEK", "SEK", None),
        ("1000 SEK", "USD", ConversionError),
        ("0 SEK", "SEK", None),
        ("0 SEK", "USD", ConversionError),
        ("0", "SEK", None),
        ("0", "USD", None),
        (-1984.51, "SEK", None),
        ("USD -1984.51", "USD", None),
        ("-1984.51 USD ", "USD", None),
        ("-1984.51 USD USD", "USD", ConversionError),
        (Money(1, currency="USD"), None, None),
        (Money(1), "USD", None),
        (Money(1, currency="USD"), "USD", None),
        (Money("4711.00 USD", currency="USD"), "USD", None),
        (Money("4711.00"), "USD", None),
        (Money("4711.00 SEK"), "USD", None),
        (None, None, ConversionError),
        (False, None, ConversionError),
        (True, None, ConversionError),
        ("X", None, ConversionError),
        (b"1", None, ConversionError),
        (b"1.00", None, ConversionError),
        (Decimal("1.51"), None, None),
        (1, 1, ConversionError),
        (1, True, ConversionError),
        (1, ";;;", ConversionError),
        ("1 ;;;", None, ConversionError),
        (";;; 1", None, ConversionError),
        (Money(1, from_sub_units=True), None, None),
        (Money(1.50, from_sub_units=True), None, None),
        (Money("1.50", from_sub_units=True), None, None),
        (Money(Decimal("150"), from_sub_units=True), None, None),
        (Money(Money("150"), from_sub_units=True), None, None),
        (Money(100), Currency.JPY, None),
        ("999999999999999999.999999999", None, None),
        ("-999999999999999999.999999999", None, None),
        ("999999999999999999.9999999999", None, ConversionError),
        ("-999999999999999999.9999999999", None, ConversionError),
        ("1000000000000000000", None, ConversionError),
        ("-1000000000000000000", None, ConversionError),
        ("Infinity", None, ConversionError),
        ("-Infinity", None, ConversionError),
        ("NaN", None, ConversionError),
        ("-Nan", None, ConversionError),
        ("1,00 SEK", None, ConversionError),
        (Decimal("Infinity"), None, ConversionError),
        (Decimal("-Infinity"), None, ConversionError),
        (Decimal("NaN"), None, ConversionError),
        (b"\n\x03EUR\x10\x01\x18\x80\xca\xb5\xee\x01", None, None),
        (b"\n\x03EUR\x10\x01\x18\x80\xca\xb5\xee\x01", "EUR", None),
        (b"\n\x03EUR\x10\x01\x18\x80\xca\xb5\xee\x01", "SEK", ConversionError),
        (b"\x10\xe7$", None, None),
        (b"\x10\xe7$ SEK", None, ConversionError),
        ('{"value": "31338.13", "currency_code": "NOK"}', None, None),
        (b'{"value": "31338.13", "currency_code": "NOK"}', None, None),
        (b'{"value": "31338.13", "currency_code": "NOK"}', "NOK", None),
        (b'{"value": "31338.13", "currency_code": "NOK"}', "EUR", ConversionError),
        (b'{"val": "31338.13"}', None, ConversionError),
        (b'{"val": "31338.13"', None, ConversionError),
        (b"{1}", None, ConversionError),
        ("{1}", None, ConversionError),
        (MoneyProtoMessage.FromString(b"\n\x03EUR\x10\x01\x18\x80\xca\xb5\xee\x01"), None, None),
        (MoneyProtoMessage.FromString(b""), None, None),
    ],
)
def test_input_values(amount: Any, currency: Any, exception_expected: Optional[Exception]) -> None:
    try:
        m = Money(amount, currency=currency)
        if exception_expected:
            assert False, "Exception expected"
        assert m is not None
    except Exception as ex:
        if not exception_expected:
            raise
        if not isinstance(ex, exception_expected):
            raise

    assert True


def test_object_input() -> None:
    class ThirdPartyMoney:
        amount: int
        currency: Optional[str]

        def __init__(self, amount: str, currency: Optional[str] = None) -> None:
            self.amount = Decimal(amount)
            self.currency = currency

        def __str__(self) -> str:
            amount = self.amount
            if self.currency:
                return f"{self.currency} {amount:.2f}"
            return f"{amount:.2f}"

    m = Money(ThirdPartyMoney("0"))
    assert m.amount == Decimal("0")
    assert str(m) == "0.00"

    m = Money(ThirdPartyMoney("1"))
    assert m.amount == Decimal("1")
    assert str(m) == "1.00"

    m = Money(ThirdPartyMoney("1.50"))
    assert m.amount == Decimal("1.50")
    assert str(m) == "1.50"

    m = Money(ThirdPartyMoney("1.5000"))
    assert m.amount == Decimal("1.5000")
    assert str(m) == "1.50"

    m = Money(ThirdPartyMoney("1.3333"))
    assert m.amount == Decimal("1.3333")
    assert str(m) == "1.3333"

    m = Money(ThirdPartyMoney("1.6666"))
    assert m.amount == Decimal("1.6666")
    assert str(m) == "1.6666"

    m = Money(ThirdPartyMoney("1.6666", "SEK"))
    assert m.amount == Decimal("1.6666")
    assert str(m) == "1.6666 SEK"

    m = Money(ThirdPartyMoney("1.6666", "SEK"), currency="SEK")
    assert m.amount == Decimal("1.6666")
    assert str(m) == "1.6666 SEK"

    m = Money(ThirdPartyMoney("1.6666"), currency="SEK")
    assert m.amount == Decimal("1.6666")
    assert str(m) == "1.6666 SEK"

    with pytest.raises(ConversionError):
        Money(ThirdPartyMoney("1.6666", "USD"), currency="SEK")


def test_dumb_object_input() -> None:
    class ThirdPartyMoney:
        amount: Any
        currency: Optional[str]
        output: Optional[str]

        def __init__(self, amount: Any, currency: Optional[str] = None, output: Optional[str] = None) -> None:
            self.amount = amount
            self.currency = currency
            self.output = output

        def __str__(self) -> str:
            if self.output:
                return self.output
            amount = self.amount
            if self.currency:
                return f"{self.currency} {amount:.2f}"
            return f"{amount}"

    m = Money(ThirdPartyMoney("1338.4711", "EUR"))
    assert m.amount == Decimal("1338.4711")
    assert str(m) == "1338.4711 EUR"

    m = Money(ThirdPartyMoney(50))
    assert m.amount == Decimal(50)
    assert str(m) == "50.00"

    with pytest.raises(ConversionError):
        Money(ThirdPartyMoney(None))

    m = Money(ThirdPartyMoney(1, output="1338.4711 EUR"))
    assert m.amount == Decimal("1.00")
    assert str(m) == "1.00 EUR"

    m = Money(ThirdPartyMoney(1, output="1338.4711"))
    assert m.amount == Decimal("1.00")
    assert str(m) == "1.00"

    m = Money(ThirdPartyMoney(1, output="1338.4711"), currency="SEK")
    assert m.amount == Decimal("1.00")
    assert str(m) == "1.00 SEK"

    m = Money(ThirdPartyMoney(1, output="USD 1338.4711"))
    assert m.amount == Decimal("1.00")
    assert str(m) == "1.00 USD"

    m = Money(ThirdPartyMoney(1, output="USD USD"))
    assert m.amount == Decimal("1.00")
    assert str(m) == "1.00"

    m = Money(ThirdPartyMoney(None, output="1338.4711 EUR"))
    assert m.amount == Decimal("1338.4711")
    assert str(m) == "1338.4711 EUR"

    with pytest.raises(ConversionError):
        Money(ThirdPartyMoney(None, output="USD USD"))


def test_units_input() -> None:
    assert Money(units=0, nanos=0) == 0
    assert Money(units=0) == 0
    assert Money(nanos=0) == 0
    assert Money(units=0, nanos=1) == Money("0.000000001")
    assert Money(nanos=2) == Money("0.000000002")
    assert Money(nanos=-2) == Money("-0.000000002")
    assert Money(units=4711) == Money(4711)
    assert Money(units=-4711) == Money(-4711)
    assert Money(units=1, nanos=750000000) == Money("1.75")
    assert Money(units=0, nanos=100000000) == Money("0.1")
    assert Money(units=-1, nanos=-750000000) == Money("-1.75")
    assert Money(units=13381339, nanos=5005335) == Money("13381339.005005335")
    assert Money(units=999999999999999999, nanos=999999999) == Money("999999999999999999.999999999")
    assert Money(units=-999999999999999999, nanos=-999999999) == Money("-999999999999999999.999999999")

    assert Money(units=1338, amount=1338) == Money(1338)
    assert Money(units=1338, nanos=250000000, amount=Decimal("1338.25")) == Money("1338.25")
    assert Money(units=1338, nanos=250000000, amount="1338.25 SEK") == Money("1338.25", currency="SEK")

    with pytest.raises(ConversionError):
        Money(units=-1, nanos=750000000)

    with pytest.raises(ConversionError):
        Money(units=1, nanos=-1)

    with pytest.raises(ConversionError):
        Money(nanos=1000000000)

    with pytest.raises(ConversionError):
        Money(units=1000000000000000000)

    with pytest.raises(ConversionError):
        Money(units=1338, amount=1337)

    with pytest.raises(ConversionError):
        Money(units=1338, nanos=250000000, amount=1338)

    with pytest.raises(ConversionError):
        Money(units=1338, nanos=250000000, amount="1338")


def test_currency_code_input() -> None:
    assert str(Money(1, currency_code="SEK")) == "1.00 SEK"
    assert str(Money(1, currency=Currency.SEK, currency_code="SEK")) == "1.00 SEK"
    assert str(Money(1, currency="SEK", currency_code="SEK")) == "1.00 SEK"

    with pytest.raises(ConversionError):
        Money(1, currency=Currency.JPY, currency_code="SEK")

    with pytest.raises(ConversionError):
        Money(1, currency_code=Currency.JPY)

    with pytest.raises(ConversionError):
        Money(1, currency=None, currency_code=Currency.JPY)

    assert str(Money(1, currency=None, currency_code="")) == "1.00"


def test_value_input() -> None:
    assert str(Money(value="4711.00 SEK")) == "4711.00 SEK"
    assert str(Money(value="4711.00 SEK", currency_code="SEK")) == "4711.00 SEK"
    assert str(Money(value="4711.00 SEK", currency=Currency.SEK)) == "4711.00 SEK"
    assert str(Money(value="4711.00 SEK", currency=Currency.SEK, currency_code="SEK")) == "4711.00 SEK"
    assert str(Money(value="4711.00", currency_code="SEK")) == "4711.00 SEK"
    assert str(Money(value="4711.00", currency=Currency.SEK)) == "4711.00 SEK"
    assert str(Money(value="4711.00")) == "4711.00"

    with pytest.raises(ConversionError):
        assert Money(value="4711.00 SEK", currency_code="JPY")

    with pytest.raises(ConversionError):
        assert Money(value="4711.00 SEK", currency=Currency.JPY)


@pytest.mark.parametrize(
    "money_input, str_output, units, nanos, proto_currency, currency_code, decimal_input, protobuf_bytes",
    [
        ("303.11 USD", "303.11 USD", 303, 110000000, "USD", "USD", "303.11", b"\n\x03USD\x10\xaf\x02\x18\x80\xef\xb94"),
        ("0 SEK", "0.00 SEK", 0, 0, "SEK", "SEK", "0", b"\n\x03SEK"),
        ("0.14999", "0.14999", 0, 149990000, "", None, "0.14999", b"\x18\xf0\xd4\xc2G"),
        (0.14999, "0.14999", 0, 149990000, "", None, "0.14999", b"\x18\xf0\xd4\xc2G"),
        (0, "0.00", 0, 0, "", None, "0", b""),
        (4711.33, "4711.33", 4711, 330000000, "", None, "4711.33", b"\x10\xe7$\x18\x80\xcd\xad\x9d\x01"),
        (
            "4711.33159263 EUR",
            "4711.33159263 EUR",
            4711,
            331592630,
            "EUR",
            "EUR",
            "4711.33159263",
            b"\n\x03EUR\x10\xe7$\x18\xb6\xe7\x8e\x9e\x01",
        ),
        ("-0.001", "-0.001", 0, -1000000, "", None, "-0.001", b"\x18\xc0\xfb\xc2\xff\xff\xff\xff\xff\xff\x01"),
        (-0.001, "-0.001", 0, -1000000, "", None, "-0.001", b"\x18\xc0\xfb\xc2\xff\xff\xff\xff\xff\xff\x01"),
        (
            "-99 DKK",
            "-99.00 DKK",
            -99,
            0,
            "DKK",
            "DKK",
            "-99",
            b"\n\x03DKK\x10\x9d\xff\xff\xff\xff\xff\xff\xff\xff\x01",
        ),
        (
            "-1.00000502",
            "-1.00000502",
            -1,
            -5020,
            "",
            None,
            "-1.00000502",
            b"\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x18\xe4\xd8\xff\xff\xff\xff\xff\xff\xff\x01",
        ),
        (
            -1.00000502,
            "-1.00000502",
            -1,
            -5020,
            "",
            None,
            "-1.00000502",
            b"\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x18\xe4\xd8\xff\xff\xff\xff\xff\xff\xff\x01",
        ),
        (
            Money("90909.999999999", currency=Currency.SEK),
            "90909.999999999 SEK",
            90909,
            999999999,
            "SEK",
            "SEK",
            "90909.999999999",
            b"\n\x03SEK\x10\x9d\xc6\x05\x18\xff\x93\xeb\xdc\x03",
        ),
        (
            "90909.999999999 SEK",
            "90909.999999999 SEK",
            90909,
            999999999,
            "SEK",
            "SEK",
            "90909.999999999",
            b"\n\x03SEK\x10\x9d\xc6\x05\x18\xff\x93\xeb\xdc\x03",
        ),
        (
            "-90909.999999999 SEK",
            "-90909.999999999 SEK",
            -90909,
            -999999999,
            "SEK",
            "SEK",
            "-90909.999999999",
            b"\n\x03SEK\x10\xe3\xb9\xfa\xff\xff\xff\xff\xff\xff\x01\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            "0.999999999 USD",
            "0.999999999 USD",
            0,
            999999999,
            "USD",
            "USD",
            "0.999999999",
            b"\n\x03USD\x18\xff\x93\xeb\xdc\x03",
        ),
        (0.999999999, "0.999999999", 0, 999999999, "", None, "0.999999999", b"\x18\xff\x93\xeb\xdc\x03"),
        ("0.9999999995 USD", "1.00 USD", 1, 0, "USD", "USD", "1", b"\n\x03USD\x10\x01"),
        (0.9999999995, "1.00", 1, 0, "", None, "1", b"\x10\x01"),
        ("0.000000001 USD", "0.000000001 USD", 0, 1, "USD", "USD", "0.000000001", b"\n\x03USD\x18\x01"),
        (0.000000001, "0.000000001", 0, 1, "", None, "0.000000001", b"\x18\x01"),
        ("1.000000001", "1.000000001", 1, 1, "", None, "1.000000001", b"\x10\x01\x18\x01"),
        (1.000000001, "1.000000001", 1, 1, "", None, "1.000000001", b"\x10\x01\x18\x01"),
        ("1.0000000005", "1.000000001", 1, 1, "", None, "1.000000001", b"\x10\x01\x18\x01"),
        (1.0000000005, "1.000000001", 1, 1, "", None, "1.000000001", b"\x10\x01\x18\x01"),
        ("1.0000000014", "1.000000001", 1, 1, "", None, "1.000000001", b"\x10\x01\x18\x01"),
        (1.0000000014, "1.000000001", 1, 1, "", None, "1.000000001", b"\x10\x01\x18\x01"),
        ("1.0000000015", "1.000000002", 1, 2, "", None, "1.000000002", b"\x10\x01\x18\x02"),
        (1.0000000015, "1.000000002", 1, 2, "", None, "1.000000002", b"\x10\x01\x18\x02"),
        ("1.0000000004", "1.00", 1, 0, "", None, "1", b"\x10\x01"),
        (1.0000000004, "1.00", 1, 0, "", None, "1", b"\x10\x01"),
        ("0.0000000005 USD", "0.000000001 USD", 0, 1, "USD", "USD", "0.000000001", b"\n\x03USD\x18\x01"),
        (0.0000000005, "0.000000001", 0, 1, "", None, "0.000000001", b"\x18\x01"),
        ("0.0000000001 USD", "0.00 USD", 0, 0, "USD", "USD", "0", b"\n\x03USD"),
        (0.0000000001, "0.00", 0, 0, "", None, "0", b""),
        (
            "-0.999999999 USD",
            "-0.999999999 USD",
            0,
            -999999999,
            "USD",
            "USD",
            "-0.999999999",
            b"\n\x03USD\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            -0.999999999,
            "-0.999999999",
            0,
            -999999999,
            "",
            None,
            "-0.999999999",
            b"\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            "-0.9999999990 USD",
            "-0.999999999 USD",
            0,
            -999999999,
            "USD",
            "USD",
            "-0.999999999",
            b"\n\x03USD\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            -0.9999999990,
            "-0.999999999",
            0,
            -999999999,
            "",
            None,
            "-0.999999999",
            b"\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            "-0.9999999994 USD",
            "-0.999999999 USD",
            0,
            -999999999,
            "USD",
            "USD",
            "-0.999999999",
            b"\n\x03USD\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            -0.9999999994,
            "-0.999999999",
            0,
            -999999999,
            "",
            None,
            "-0.999999999",
            b"\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            "-0.99999999949 USD",
            "-0.999999999 USD",
            0,
            -999999999,
            "USD",
            "USD",
            "-0.999999999",
            b"\n\x03USD\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            -0.99999999949,
            "-0.999999999",
            0,
            -999999999,
            "",
            None,
            "-0.999999999",
            b"\x18\x81\xec\x94\xa3\xfc\xff\xff\xff\xff\x01",
        ),
        (
            "-0.9999999995 USD",
            "-1.00 USD",
            -1,
            0,
            "USD",
            "USD",
            "-1",
            b"\n\x03USD\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01",
        ),
        (-0.9999999995, "-1.00", -1, 0, "", None, "-1", b"\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01"),
        ("-1.9999999995", "-2.00", -2, 0, "", None, "-2", b"\x10\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01"),
        (-1.9999999995, "-2.00", -2, 0, "", None, "-2", b"\x10\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01"),
        (
            "-1.4999999995",
            "-1.50",
            -1,
            -500000000,
            "",
            None,
            "-1.50",
            b"\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x18\x80\xb6\xca\x91\xfe\xff\xff\xff\xff\x01",
        ),
        (
            -1.4999999995,
            "-1.50",
            -1,
            -500000000,
            "",
            None,
            "-1.50",
            b"\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x18\x80\xb6\xca\x91\xfe\xff\xff\xff\xff\x01",
        ),
        (
            "-1.0999999905",
            "-1.099999991",
            -1,
            -99999991,
            "",
            None,
            "-1.099999991",
            b"\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x18\x89\xbe\xa8\xd0\xff\xff\xff\xff\xff\x01",
        ),
        (
            -1.0999999905,
            "-1.099999991",
            -1,
            -99999991,
            "",
            None,
            "-1.099999991",
            b"\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x18\x89\xbe\xa8\xd0\xff\xff\xff\xff\xff\x01",
        ),
        (
            "-0.0000000005 USD",
            "-0.000000001 USD",
            0,
            -1,
            "USD",
            "USD",
            "-0.000000001",
            b"\n\x03USD\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01",
        ),
        (
            -0.0000000005,
            "-0.000000001",
            0,
            -1,
            "",
            None,
            "-0.000000001",
            b"\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01",
        ),
        ("-0.0000000001 USD", "0.00 USD", 0, 0, "USD", "USD", "0", b"\n\x03USD"),
        (-0.0000000001, "0.00", 0, 0, "", None, "0", b""),
    ],
)
def test_protobuf_input(
    money_input: Any,
    str_output: str,
    units: int,
    nanos: int,
    proto_currency: str,
    currency_code: Optional[str],
    decimal_input: str,
    protobuf_bytes: bytes,
) -> None:
    m1 = Money(money_input)

    proto_output = m1.as_protobuf()
    assert proto_output.units == units
    assert proto_output.nanos == nanos
    assert proto_output.currency_code is not None
    assert proto_output.currency_code == proto_currency
    assert proto_output.SerializeToString() == protobuf_bytes

    m2 = Money(proto_output.SerializeToString())
    assert str(m2) == str_output
    assert m2.as_decimal() == Decimal(decimal_input)
    assert m2.units == units
    assert m2.nanos == nanos
    if currency_code is None:
        assert m2.currency is None
    else:
        assert m2.currency == currency_code
    if currency_code is None:
        assert m2.currency is None
    else:
        assert m2.currency_code == currency_code
    assert m2.as_protobuf().currency_code == proto_currency

    m3 = Money(proto_output)
    assert str(m3) == str_output
    assert m3.as_decimal() == Decimal(decimal_input)
    assert m3.units == units
    assert m3.nanos == nanos
    if currency_code is None:
        assert m3.currency is None
    else:
        assert m3.currency == currency_code
    if currency_code is None:
        assert m3.currency is None
    else:
        assert m3.currency_code == currency_code
    assert m3.as_protobuf().currency_code == proto_currency
    assert m3 == m2
