# `stockholm` — `Money` for Python 3
[![pypi](https://badge.fury.io/py/stockholm.svg)](https://pypi.python.org/pypi/stockholm/)
[![Made with Python](https://img.shields.io/pypi/pyversions/stockholm)](https://www.python.org/)
[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/stockholm)
[![MIT License](https://img.shields.io/github/license/kalaspuff/stockholm.svg)](https://github.com/kalaspuff/stockholm/blob/master/LICENSE)
[![Code coverage](https://codecov.io/gh/kalaspuff/stockholm/branch/master/graph/badge.svg)](https://codecov.io/gh/kalaspuff/stockholm/tree/master/stockholm)

*Library for formatting and performing arithmetic and comparison operations on monetary amounts. Also with support for currency handling, exchange and network transport structure generation as well as parsing.*

An up to date human friendly and flexible approach for development with any kind of monetary amounts. No more working with floats or having to deal with having to think about values in subunits.

Basically a high-end `Money` class for Python 3.x. This is a library to be used by backend and frontend API coders of fintech companies, web merchants or subscription services. It's great for calculations of amounts while keeping a great level of precision or producing output for transport layers as well as having a robust and easy way to import/export values in JSON or Protocol Buffers and the alike. 

*A simple, yet powerful way of coding with money.*

---

#### `from stockholm import Money`
The `stockholm.Money` object has full arithmetic support together with `int`, `float`, `Decimal`, other `Money` objects as well as `string`. The `stockholm.Money` object also supports complex string formatting functionality for easy debugging and a clean coding pattern.

#### `from stockholm import Currency`
Currencies to monetary amounts can be specified using either currencies built with the `stockholm.Currency` metaclasses or simply by specifying the currency ticker as a string (for example `"SEK"` or `"EUR"`) when creating a new `Money` object.

Currencies using the `stockholm.Currency` metaclasses can hold additional options, such as default number of decimals in string output. Note that the amounts behind the scenes actually uses the same precision and backend as `Decimal` values and can as well be interchangable with such values, as such they are way more exact to do calculations with than floating point values.


## Installation with `pip`
Like you would install any other Python package, use `pip`, `poetry`, `pipenv` or your weapon of choice.
```
$ pip install stockholm
```


## Usage and examples

#### Arithmetics - fully supported
*Full arithmetic support with different types, backed by `Decimal` for dealing with rounding errors, while also keeping the monetary amount fully currency aware.*
```python
from stockholm import Money

money = Money("4711.50", currency="SEK")
print(money)
# 4711.50 SEK

output = (money + 100) * 3 + Money(50)
print(output)
# 14484.50 SEK

print(output / 5)
# 2896.90 SEK

print(round(output / 3, 4))
# 4828.1667 SEK

print(round(output / 3, 1))
# 4828.20 SEK
```

#### Formatting / Advanced string formatting
*Advanced string formatting functionality.*
```python
from stockholm import Money

jpy_money = Money(1352953, "JPY")
exchange_rate = Money("0.08861326")
sek_money = Money(jpy_money * exchange_rate, "SEK")

print(f"I have {jpy_money:,.0m} which equals around {sek_money:,.2m}")
print(f"The exchange rate is {exchange_rate} ({jpy_money:c} -> {sek_money:c})")
# I have 1,352,953 JPY which equals around 119,889.58 SEK
# The exchange rate is 0.08861326 (JPY -> SEK)

# Standard string format uses default min decimals up to 9 decimals
print(f"{sek_money}")  # 119889.57595678 SEK

# Format type "f" works the same way as formatting a float or Decimal
print(f"{jpy_money:.0f}")  # 1352953
print(f"{sek_money:.2f}")  # 119889.58
print(f"{sek_money:.1f}")  # 119889.6
print(f"{sek_money:.0f}")  # 119890

# Format type "m" works as "f" but includes the currency in string output
print(f"{sek_money:.2m}")  # 119889.57 SEK
print(f"{sek_money:.4m}")  # 119889.5760 SEK
print(f"{sek_money:+,.4m}")  # +119,889.5760 SEK

# An uppercase "M" puts the currency ticker in front of the amount
print(f"{sek_money:.4M}")  # SEK 119889.5760

# Format type "c" will just output the currency used in the monetary amount
print(f"{sek_money:c}")  # SEK
```

*Use `stockholm.Currency` types for proper defaults of minimum number of decimal digits to output in strings, etc. All ISO 4217 currency codes implemented, see https://github.com/kalaspuff/stockholm/blob/master/stockholm/currency.py for the full list.*
```python
from stockholm import Currency, Money, get_currency
from stockholm.currency import JPY, SEK, EUR, IQD, USDCoin, Bitcoin

# Most currencies has a minimum default digits set to 2 in strings
print(Money(4711, SEK))  # 4711.00 SEK
print(Money(4711, EUR))  # 4711.00 EUR

# The stockholm.currency.JPY has a minimum default digits set to 0
print(Money(4711, JPY))  # 4711 JPY

# Some currencies even has a minimum default of 3 or 4 digits
print(Money(4711, IQD))  # 4711.000 IQD

# Some complex non ISO 4217 currencies, assets or tokens may define
# their own ticker, for example a "USD Coin" uses the ticker "USDC"
print(Money(4711, USDCoin))  # 4711.00 USDC
print(Money(4711, Bitcoin))  # 4711.00 BTC

# You can also use the shorthand stockholm.Currency object which
# holds all ISO 4217 three character codes as objects.
print(Money(1338, Currency.JPY))  # 1338 JPY

# or call the get_currency function
print(Money(1338, get_currency("JPY")))  # 1338 JPY

```

#### Input data types in flexible variants
*Flexible ways for assigning values to a monetary amount using many different input data types and methods.*
```python
from decimal import Decimal
from stockholm import Money

Money(100, currency="EUR")
# <stockholm.Money: "100.00 EUR">

Money("1338 USD")
# <stockholm.Money: "1338.00 USD">

Money("0.5")
# <stockholm.Money: "0.50">

amount = Decimal(5000) / 3
Money(amount, currency="XDR")
# <stockholm.Money: "1666.666666667 XDR">

money = Money("0.30285471")
Money(money, currency="BTC")
# <stockholm.Money: "0.30285471 BTC">

cents_as_str = "471100"
money = Money(cents_as_str, currency="USD", from_sub_units=True)
# <stockholm.Money: "4711.00 USD">
money.sub_units
# Decimal('471100')
```

#### List arithmetics - summary of monetary amounts in list
*Adding several monetary amounts from a list.*
```python
from stockholm import Money

amounts = [
    Money(1),
    Money("1.50"),
    Money("1000"),
]

# Use Money.sum to deal with complex values of different data types
Money.sum(amounts)
# <stockholm.Money: "1002.50">

# Built-in sum may also be used (if only working with monetary amounts)
sum(amounts)
# <stockholm.Money: "1002.50">
```

#### Conversion for other transport medium (for example Protocol Buffers or JSON)
*Easily splittable into `units` and `nanos` for transport in network medium, for example using the [`google.type.Money` protobuf definition](https://github.com/googleapis/googleapis/blob/master/google/type/money.proto) when using Protocol Buffers.*
```python
from stockholm import Money

money = Money("22583.75382", "SEK")
money.units, money.nanos, money.currency_code
# (22583, 753820000, 'SEK')

# or vice versa
Money(units=22583, nanos=753820000, currency="SEK")
# <stockholm.Money: "22583.75382 SEK">
```

*Monetary amounts can also be exported to `dict` as well as created with `dict` value input, which can be great to for example transport a monetary value in JSON.*
```python
from stockholm import Money

money = Money("4711.75", "SEK")
dict(money)  # or by using: money.asdict()
# {'value': '4711.75 SEK', 'units': 4711, 'nanos': 750000000, 'currency_code': 'SEK'}

# A monetary amount object can be created from a dict either by passing dict directly
# to the Money() constructor or by using Money.from_dict(dict_input). Not all values
# needs to be available in the input dict, either "units", "nanos", "value" or "amount"
# should be specified or any combination of them, as long as values would result in the
# same output monetary value.
money = Money.from_dict({
    "value": "4711.75 SEK",
    "units": 4711,
    "nanos": 750000000,
    "currency_code": "SEK"
})
# <stockholm.Money: "4711.75 SEK">
```


## Acknowledgements
Built with inspiration from https://github.com/carlospalol/money and https://github.com/vimeo/py-money
