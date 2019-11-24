from typing import Any, Optional

from decimal import Decimal
import pytest

from stockholm import Money, ConversionError


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
        (Money(1, is_cents=True), None, None),
        (Money(1.50, is_cents=True), None, None),
        (Money("1.50", is_cents=True), None, None),
        (Money(Decimal("150"), is_cents=True), None, None),
        (Money(Money("150"), is_cents=True), None, None),
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
