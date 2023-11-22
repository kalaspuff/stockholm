from decimal import Decimal

from pydantic import BaseModel

from stockholm import Currency, Money
from stockholm.currency import JPY, USD
from stockholm.types import (
    ConvertibleToCurrency,
    ConvertibleToMoney,
    ConvertibleToMoneyWithRequiredCurrency,
    ConvertibleToNumber,
)


def test_pydantic_model_money_field() -> None:
    class TestModel(BaseModel):
        value: Money

    assert TestModel(value=Money(100, "JPY")).value == Money(100, "JPY")
    assert TestModel(value=Money(100, "SEK")).value != Money(100, "JPY")
    assert TestModel(value=Money(100, "SEK")).value.currency == "SEK"

    assert TestModel(value=Money(4711.42)).value.amount == Decimal("4711.42")

    assert TestModel(value=Money(4711.42, "JPY")).value.amount == Decimal("4711.42")
    assert TestModel(value=Money(4711.42, "JPY")).value.currency == "JPY"


def test_pydantic_model_currency_field() -> None:
    class TestModel(BaseModel):
        currency: Currency

    assert TestModel(currency=USD).currency.ticker == "USD"
    assert TestModel(currency=Currency.SEK).currency.ticker == "SEK"
    assert TestModel(currency=Currency("EUR")).currency.ticker == "EUR"

    assert TestModel(currency=Currency.NOK).currency.decimal_digits == 2
    assert TestModel(currency=JPY).currency.decimal_digits == 0
    assert TestModel(currency=Currency.ILP).currency.decimal_digits == 3
    assert TestModel(currency=Currency("ILP")).currency.decimal_digits == 3


def test_pydantic_convertible_model() -> None:
    class TestConvertibleModel(BaseModel):
        money: ConvertibleToMoney
        money_with_currency: ConvertibleToMoneyWithRequiredCurrency
        number: ConvertibleToNumber
        currency: ConvertibleToCurrency

    m = TestConvertibleModel(
        money="100.45", money_with_currency={"amount": 42.999, "currency": "SEK"}, number=42, currency="JPY"
    )

    assert m.money.amount == Decimal("100.45")
    assert m.money_with_currency.currency == "SEK"
    assert m.number.units == 42
    assert m.currency == "JPY"
    assert m.currency.decimal_digits == 0

    assert m.money_with_currency.as_dict() == {
        "value": "42.999 SEK",
        "units": 42,
        "nanos": 999000000,
        "currency_code": "SEK",
    }

    assert m.number.as_dict() == {
        "value": "42",
        "units": 42,
        "nanos": 0,
    }
