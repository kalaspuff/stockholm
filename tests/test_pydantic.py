import json
from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from stockholm import Currency, Money, get_currency
from stockholm.currency import JPY, USD, BaseCurrency
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

    assert json.loads(m.model_dump_json()) == {
        "money": {"value": "100.45", "units": 100, "nanos": 450000000, "currency_code": None},
        "money_with_currency": {"value": "42.999 SEK", "units": 42, "nanos": 999000000, "currency_code": "SEK"},
        "number": {"value": "42", "units": 42, "nanos": 0},
        "currency": "JPY",
    }

    assert m == TestConvertibleModel.model_validate_json(m.model_dump_json())
    assert m.model_dump_json() == TestConvertibleModel.model_validate_json(m.model_dump_json()).model_dump_json()


def test_validate_money() -> None:
    def validate_money(value: Any) -> Money:
        return Money(value)

    assert Money._validate(-0.01, validate_money).as_dict() == {
        "value": "-0.01",
        "units": 0,
        "nanos": -10000000,
        "currency_code": None,
    }
    assert Money._validate("4711.00499 EUR", validate_money).as_dict() == {
        "value": "4711.00499 EUR",
        "units": 4711,
        "nanos": 4990000,
        "currency_code": "EUR",
    }
    assert Money._validate({"units": 42, "nanos": 15000000, "currency": "USD"}, validate_money).as_dict() == {
        "value": "42.015 USD",
        "units": 42,
        "nanos": 15000000,
        "currency_code": "USD",
    }


def test_validate_currency() -> None:
    def validate_currency_code(value: Any) -> BaseCurrency:
        return get_currency(str(value))

    assert Currency._validate(Currency.USD, validate_currency_code).ticker == "USD"
    assert Currency._validate("JPY", validate_currency_code).ticker == "JPY"
    assert Currency._validate(Currency.USD, validate_currency_code).decimal_digits == 2
    assert Currency._validate("JPY", validate_currency_code).decimal_digits == 0
