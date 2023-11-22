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


class TestModel(BaseModel):
    value: Money
    currency: Currency


assert TestModel(value=Money(4711.42, "JPY"), currency=USD).value.amount == Decimal("4711.42")
assert TestModel(value=Money(4711.42, "JPY"), currency=Currency.SEK).value.currency == "JPY"
assert TestModel(value=Money(4711.42, "JPY"), currency=Currency("EUR")).value.amount == Decimal("4711.42")

assert TestModel(value=Money(4711.42, "JPY"), currency=USD).currency.ticker == "USD"
assert TestModel(value=Money(4711.42, "JPY"), currency=Currency.SEK).currency.ticker == "SEK"
assert TestModel(value=Money(4711.42, "JPY"), currency=Currency("EUR")).currency.ticker == "EUR"

assert TestModel(value=Money(4711.42, "JPY"), currency=Currency.NOK).currency.decimal_digits == 2
assert TestModel(value=Money(4711.42, "JPY"), currency=JPY).currency.decimal_digits == 0
assert TestModel(value=Money(4711.42, "JPY"), currency=Currency.ILP).currency.decimal_digits == 3
assert TestModel(value=Money(4711.42, "JPY"), currency=Currency("ILP")).currency.decimal_digits == 3


class TestConvertibleModel(BaseModel):
    money: ConvertibleToMoney
    money_with_currency: ConvertibleToMoneyWithRequiredCurrency
    number: ConvertibleToNumber
    currency: ConvertibleToCurrency


m1 = TestConvertibleModel(
    money="100.45", money_with_currency={"amount": 42.999, "currency": "SEK"}, number=42, currency="JPY"
)

assert m1.money.amount == Decimal("100.45")
assert m1.money_with_currency.currency == "SEK"
assert m1.number.units == 42
assert m1.currency.ticker == "JPY"
assert m1.currency.decimal_digits == 0

assert m1.money_with_currency.as_dict() == {
    "value": "42.999 SEK",
    "units": 42,
    "nanos": 999000000,
    "currency_code": "SEK",
}

assert m1.number.as_dict() == {
    "value": "42",
    "units": 42,
    "nanos": 0,
}
