# `stockholm`

**This brings a fully featured `Money` class for Python 3 – `stockholm.Money`.**

[![Python package](https://github.com/kalaspuff/stockholm/workflows/Python%20package/badge.svg)](https://github.com/kalaspuff/stockholm/actions/workflows/pythonpackage.yml)
[![pypi](https://badge.fury.io/py/stockholm.svg)](https://pypi.python.org/pypi/stockholm/)
[![Made with Python](https://img.shields.io/pypi/pyversions/stockholm)](https://www.python.org/)
[![MIT License](https://img.shields.io/github/license/kalaspuff/stockholm.svg)](https://github.com/kalaspuff/stockholm/blob/master/LICENSE)
[![Code coverage](https://codecov.io/gh/kalaspuff/stockholm/branch/master/graph/badge.svg)](https://codecov.io/gh/kalaspuff/stockholm/tree/master/stockholm)

*Library for formatting and performing arithmetic and comparison operations on monetary amounts. Also with support for currency handling, rates, exchange and serialization + deserialization for when transporting monetary amount data across network layers (built-in data generation and parsing).* 💰

### A library for monetary amounts

* Combining an amount with a currency to create a monetary amount, as they usually should be read, written and transported together.
* Able to work with a plethora of different source types. Human friendly approach with developer experience in mind.
* Get rid of the gotchas if otherwise using `decimal.Decimal`. Sensible rounding by default. Never lose precision when making arithmetic operations. String output as you would expect.
* Generate (and parse) structured data to be used in transport layers such as GraphQL or Protobuf.
* Type hinted, battle tested and supporting several versions of Python.

#### Full feature set further down, but in its simplest form 👇

```pycon
>>> Money("9001.42", currency="USD")
<stockholm.Money: "9001.42 USD">
```

![stockholm.Money](https://user-images.githubusercontent.com/89139/123852607-c9a0c380-d91c-11eb-9d47-cf7cd5751c01.png)

### Basic examples

Basically `stockholm` is a human friendly and modern `Money` class for Python 3. This is a library to be used by backend and frontend API coders of fintech companies, web merchants or subscription services. It's great for calculations of amounts while keeping a great level of precision.

```python
from stockholm import Money, Rate

loan_amount = Money("250380.00", currency="EUR")
# <stockholm.Money: "250380.00 EUR">

interest_rate = Rate(0.073)
# <stockholm.Rate: "0.073">

interest_per_day = loan_amount * (interest_rate / 365)
# <stockholm.Money: "50.076 EUR">
```

Comes with functions to produce output for transport layers as well as having a robust and easy way to import/export values in *GraphQL*, *JSON*, *Protocol Buffers*, etc.

```python
interest_per_day.asdict()
# {'value': '50.076 EUR', 'units': 50, 'nanos': 76000000, 'currency_code': 'EUR'}
```

```python
interest_per_day.asdict(keys=("amount", "currency"))
# {'amount': '50.076', 'currency': 'EUR'}
```

```python
interest_per_day.as_protobuf()
# <class 'google.type.money_pb2.Money'>
# · currency_code: "EUR"
# · units: 50
# · nanos: 76000000
```

The goal is to provide a flexible and robust package for development with any kind of monetary amounts. No more working with floats or having to deal with having to think about values in subunits for data transport layers or losing hours of sleep because of the default way that `Decimal` does rounding.

The monetary amounts can be transformed from (or into) dicts, strings, protobuf messages, json, floats, ints, Python Decimals, even other monetary amounts.

```python
from stockholm import Money, Number

gross_price = Money("319.20 SEK")
# <stockholm.Money: "319.20 SEK">

vat_rate = Number(0.25)  # 25% vat
vat_price = gross_price * vat_rate
# <stockholm.Money: "79.80 SEK">

net_price = gross_price + vat_price
# <stockholm.Money: "399.00 SEK">

total_sum = net_price * 5  # price of five items
# <stockholm.Money: "1995.00 SEK">

total_sum / 4  # total split on four people
# <stockholm.Money: "498.75 SEK">
```

Coding applications, libaries and microservices that consume and publish events that contain monetary amounts shouldn't be any harder than anything else. This package aims to ease that work. You can also use it for just numerical values of course.

#### Real life use-cases

There are times when you want to receive or publish events with monetary amounts or you need to expose an API endpoint and have a structured way to respond with balances, prices, vat, etc. without risking additional weirdness.

If you're developing a merchant solution, a ticketing service or webshop it can be great to have easy and structured interfaces for calculating orders and building summaries or reports.

#### We don't want to use `float`, but you can do more than just rely on `int` 🤔

Some may be interfacing with banking infrastructure from the 70s or 80s 😓 and has to process data in insanly old string based formats like the example below and validate sums, currencies, etc.

<p align="center">
<img width="580" alt="stockholm-parse-monetary-amounts" src="https://user-images.githubusercontent.com/89139/123870276-6588fa00-d932-11eb-9438-a4c58a44625b.png">
</p>

If any of these sounds familiar, a library for handling monetary amounts could help to structure interfaces you build – specially if you're on microservice architectures where code bases quickly gets a life of their own and teams will likely have different takes on their APIs unless strict guidelines (or utility libraries) are in place.

## The basic interfaces

### `from stockholm import Money`

The `stockholm.Money` object has full arithmetic support together with `int`, `float`, `Decimal`, other `Money` objects as well as `string`. The `stockholm.Money` object also supports complex string formatting functionality for easy debugging and a clean coding pattern.

```python
from stockholm import Money

Money("99.95 USD")
# <stockholm.Money: "99.95 USD">
```

### `from stockholm import Currency`

Currencies to monetary amounts can be specified using either currencies built with the `stockholm.Currency` metaclasses or simply by specifying the currency ticker as a string (for example `"SEK"` or `"EUR"`) when creating a new `Money` object.

Most currencies use two decimals in their default output. Some (like *JPY*) use fractions per default, and a few ones even has more than two decimals.

```python
from stockholm import Currency, Money

Money(1000, "CNY")
# <stockholm.Money: "1000.00 CNY">

Money(1000, Currency.USD)
# <stockholm.Money: "1000.00 USD">

Money(1000, Currency.JPY)
# <stockholm.Money: "1000 JPY">
```

Currencies using the `stockholm.Currency` metaclasses can hold additional options, such as default number of decimals in string output. Note that the amounts behind the scenes actually uses the same precision and backend as `Decimal` values and can as well be interchangable with such values, as such they are way more exact to do calculations with than floating point values.

### `from stockholm import Number, Rate`

The `Number` and `Rate` classes works in the same way and is similar to the `Money` class, with the exception that they cannot hold a currency type and cannot operate with sub units. Examples of when to use them could be to differentiate some values from monetary values, while still getting the benefits from the `Money` class.

Arithmetic operations between numbers and monetary `Money` values will usually result in a returned `Money` object. When instantiating a `Money` object the currency value can be overriden from the source amount, which could be useful when exchanging currencies.

```python
from stockholm import Money, Rate

jpy_money = Money(1352953, "JPY")
exchange_rate = Rate("0.08861326")
sek_money = Money(jpy_money * exchange_rate, "SEK")

print(f"I have {jpy_money:,.0m} which equals around {sek_money:,.2m}")
print(f"The exchange rate is {exchange_rate} ({jpy_money:c} -> {sek_money:c})")
# I have 1,352,953 JPY which equals around 119,889.58 SEK
# The exchange rate is 0.08861326 (JPY -> SEK)
```

## Installation with `pip`
Like you would install any other Python package, use `pip`, `poetry`, `pipenv` or your favourite tool.

```
$ pip install stockholm
```

To install with Protocol Buffers support, specify the `protobuf` extras.

```
$ pip install stockholm[protobuf]
```

## Topics in more detail

* [**Arithmetics – works with loads of compatible types – completely currency aware.**](#arithmetics---fully-supported)
* [**Instantiating a monetary amount in many flexible ways.**](#input-data-types-in-flexible-variants)
* [**Using `stockholm.Money` monetary amount with Protocol Buffers.**](#using-protocol-buffers-for-transporting-monetary-amounts-over-the-network)
* [**Conversion between dicts, JSON and values for use in GraphQL or other JSON-based API:s:**](#conversion-for-other-transport-medium-for-example-protocol-buffers-or-json)
  - [**Using dict values for input and output / having GraphQL in mind.**](#monetary-amounts-can-also-be-exported-to-dict-as-well-as-created-with-dict-value-input-which-can-be-great-to-for-example-transport-a-monetary-value-in-json)
  - [**Parsing and loading JSON data.**](#reading-or-outputting-monetary-amounts-as-json)
* [**Parameters and functions of the `stockholm.Money` object.**](#parameters-of-the-money-object)

### Arithmetics - fully supported

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

# Note that you can only do arithmetics on two monetary amounts which shares the
# same currency, monetary amounts that doesn't hold a currency at all or an
# operation between a currency aware monetary object and a value that doesn't hold
# data about a currency.
# Look at the following examples of completely legit operations.

Money("100 SEK") + Money("50 SEK")
# <stockholm.Money: "150.00 SEK">

Money("100 EUR") * 20 + 5 - 3.5
# <stockholm.Money: "2001.50 EUR">

Money("100 USD") - Money("10")
# <stockholm.Money: "90.00 USD">

Money("100") - Money("50") + 20
# <stockholm.Money: "70.00">

Money("100") + Money(2, currency="GBP")
# <stockholm.Money: "102.00 GBP">

Money("100", currency="EUR") + Money("10 EUR") - 50 + "20.51 EUR"
# <stockholm.Money: "80.51 EUR">

# And here's operations that tries to use two amounts with different currencies.

Money("100", currency="SEK") + Money("10 EUR")
# ! This results in a stockholm.exceptions.CurrencyMismatchError exception

Money(1) + Money("55 EUR") + Money(10, currency="EUR").to_currency("USD")
# ! This results in a stockholm.exceptions.CurrencyMismatchError exception

# Also note that you cannot multiply two currency aware monetary amounts by each
# other, for example say "5 EUR" * "5 EUR", that in that case would've resulted
# in "25 EUR EUR". A monetary amount can only hold one instance of currency.

Money("5 EUR") * Money("5 EUR")
# ! This results in a stockholm.exceptions.InvalidOperandError exception

```

### Formatting and advanced string formatting

Use f-string formatting for more human readable output and `money.as_string()` function to output with additional (or less) zero-padded fraction digits.

```python
from stockholm import Money

amount = Money("13384711 USD")

human_readable_amount = f"{amount:,m}"
# '13,384,711.00 USD'

amount_without_unnecessary_decimals = amount.as_string(min_decimals=0)
# '13384711 USD'
```

*Advanced string formatting functionality.*

```python
from stockholm import Money, Rate

jpy_money = Money(1352953, "JPY")
exchange_rate = Rate("0.08861326")
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

### Currency class

##### *Use `stockholm.Currency` types for proper defaults of minimum number of decimal digits to output in strings, etc. All ISO 4217 currency codes implemented, see https://github.com/kalaspuff/stockholm/blob/master/stockholm/currency.py for the full list.*

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

### Parsing input

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

# Reading values as "sub units" (multiplied by 100) can come in handy when parsing
# some older types of banking files, where all values are presented as strings in
# cents / ören / etc.
cents_as_str = "471100"
money = Money(cents_as_str, currency="USD", from_sub_units=True)
# <stockholm.Money: "4711.00 USD">
money.sub_units
# Decimal('471100')
```

### List arithmetics - summary of monetary amounts in list

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

### Conversion for other transport medium (for example Protocol Buffers or JSON)

##### *Easily splittable into `units` and `nanos` for transport in network medium, for example using the [`google.type.Money` protobuf definition](https://github.com/googleapis/googleapis/blob/master/google/type/money.proto) when using Protocol Buffers.*

```python
from stockholm import Money

money = Money("22583.75382", "SEK")
money.units, money.nanos, money.currency_code
# (22583, 753820000, 'SEK')

# or vice versa
Money(units=22583, nanos=753820000, currency="SEK")
# <stockholm.Money: "22583.75382 SEK">
```

##### *Monetary amounts can also be exported to `dict` as well as created with `dict` value input, which can be great to for example transport a monetary value in JSON.*

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

The `money.asdict()` function can be called with an optional `keys` argument, which can be used to specify a tuple of keys which shuld be used in the returned dict.

The default behaviour of `money.asdict()` is equivalent to `money.asdict(keys=("value", "units", "nanos", "currency_code"))`.

Values to use in the `keys` tuple for `stockholm.Money` objects are any combination of the following:

| key | description | return type | example |
| :-- | :---------- | :---------- | -------: |
| `value` | amount + currency code | `str` | `"9001.50 USD"`
| `units` | units of the amount | `int` | `9001` |
| `nanos` | number of nano units of the amount | `int` | `500000000` |
| `currency_code` | currency code if available | `str \| None` | `"USD"` |
| `currency` | currency code if available | `str \| None` | `"USD"` |
| `amount` | the monetary amount (excl. currency code) | `str` | `"9001.50"` |

```python
from stockholm import Money

Money("4711 USD").asdict(keys=("value", "units", "nanos", "currency_code"))
# {'value': '4711.00 USD', 'units': 4711, 'nanos': 0, 'currency_code': 'USD'}

Money("4711 USD").asdict(keys=("amount", "currency"))
# {'amount': '4711.00', 'currency': 'USD'}

Money(nanos=10).asdict(keys=("value", "currency", "units", "nanos"))
# {'value': '0.00000001', 'currency': None, 'units': 0, 'nanos': 10}
```

##### *Using Protocol Buffers for transporting monetary amounts over the network.*

```python
from stockholm import Money

# By default we're utilizing Google's protobuf message called google.type.Money, however
# the protobuf class can be overriden with your own if using similar keys and value types.
# https://github.com/googleapis/googleapis/blob/master/google/type/money.proto

money = Money("4711.75", "SEK")
money.as_protobuf()
# This will produce a protobuf object which by default holds values for units, nanos and
# currency_code as per the google.type.Money protobuf message definition.
# Use money.as_protobuf(proto_class=YourProtoClass) if you're using custom messages that
# are not of Google's proto message type.
#
# To get the exact byte output produced from the proto class, call their
# SerailizeToString() function.
money.as_protobuf().SerializeToString()
# b'\n\x03SEK\x10\xe7$\x18\x80\xaf\xd0\xe5\x02'

# Of course we can also instantiate a monetary amount object by passing a proto message,
# either by using the already parsed proto object, or by passing the byte data directly.
# If no proto_class keyword argument is specified, we'll once again default to
# google.type.Money.
money = Money.from_protobuf(b'\n\x03SEK\x10\xe7$\x18\x80\xaf\xd0\xe5\x02')
# <stockholm.Money: "4711.75 SEK">

# In another example we'll build the message just before hand to be extra descriptive
# of what's happening. The stockholm.MoneyProtobufMessage (or stockholm.protobuf.Money)
# class is a generated Python representation of the google.type.Money protobuf message
# definition. You can also use your own custom class.
from stockholm import MoneyProtobufMessage
message = MoneyProtobufMessage()
message.units = 2549
message.nanos = 990000000
message.currency_code = "USD"
# If you're using custom classes that aren't generated from google.type.Money, then pass
# your generated class as the proto_class keyword argument. In this example, it's not
# actually needed, since MoneyProtobufMessage is built from google.type.Money definitions.
money = Money.from_protobuf(message, proto_class=MoneyProtobufMessage)
# <stockholm.Money: "2549.99 USD">
message.SerializeToString()
# b'\x10\xf5\x13\x18\x80\xe7\x88\xd8\x03'

# Usually the byte data may already be parsed from your proto class into your
# proto objects, and if you're using google.type.Money in your messages you could
# pass in the object without any additional proto_class keyword.
#
# In the following example we have a message that contains a field on position 1
# named "remaining_sum", which in turn holds a google.type.Money value.
#
# Let's say the message holds the following as a parsed proto object:
# remaining_sum {
#  currency_code: "USD"
#  units: 42
# }
#
# It's binary representation is b'\n\x07\n\x03USD\x10*'.
# And the binary representation of message.remaining_sum is b'\n\x03USD\x10*'.
#
# By passing the monetary part of the message (in this case, the field remaining_sum)
# we can immediately create a monetary amount object which is currency aware.
money = Money.from_protobuf(message.remaining_sum)
# <stockholm.Money: "42.00 USD">
#
# Of course this newly instantiated montary amount object can be accessed in many
# different ways, can use arithmetics like normally, etc.
money.amount
# Decimal('42.000000000')
money.units
# 42
money.nanos
# 0
money.currency
# "USD"
money + 10
# <stockholm.Money: "52.00 USD">
money * 31 - 20 + Money("0.50")
# <stockholm.Money: "1282.50 USD">
```

##### *Reading or outputting monetary amounts as JSON*

```python
from stockholm import Money

# Outputting key-values as a dict or JSON string. For example great when sending monetary
# amounts over GraphQL or internal API:s.
money = Money(5767.50, currency="EUR")
# <stockholm.Money: "5767.50 EUR">
#
# If no keys keyword argument is specified the default keys will be used, which is
# value, units, nanos and currency_code.
money.as_json()
# '{"value": "5767.50 EUR", "units": 5767, "nanos": 500000000, "currency_code": "EUR"}'
#
# Besides value, units, nanos and currency_code, the other keys that can be specified
# are amount and currency (converted to str and equivalent to currency_code in this
# context).
money.as_json(keys=("amount", "currency_code"))
# '{"amount": "5767.500000000", "currency_code": "EUR"}'

# It's also possible directly parse a monetary amount from its incoming JSON string
Money.from_json('{"value": "5767.50 EUR", "units": 5767, "nanos": 500000000}')
# <stockholm.Money: "5767.50 EUR">
Money.from_json('{"amount": "5767.500000000", "currency_code": "EUR"}')
# <stockholm.Money: "5767.50 EUR">
```

#### Parameters of the Money object

```python
from stockholm import Currency, Money

# This is our monetary object, instantiated as 59112.50 EUR using the
# currency object stockholm.Currency.EUR, which among other things holds data
# regarding how many decimal digits should normally be printed. A monetary amount
# in EUR is usually demoninated with two decimal digits.

money = Money("59112.50", currency=Currency.EUR)
# <stockholm.Money: "59112.50 EUR">

money.amount
# Decimal('59112.50')
# Type: decimal.Decimal

money.value
# '59112.50 EUR'
# Type: string

money.units
# 59112
# Type: integer

money.nanos
# 500000000
# Type: integer

money.currency_code
# 'EUR'
# Type: Either: A string or None

money.currency
# <stockholm.Currency: "EUR">
# Type: Either: a currency object, a string (equivalent to currency_code) or None

money.sub_units
# Decimal('5911250')
# Type: decimal.Decimal

money.asdict()
# {'value': '59112.50 EUR', 'units': 59112, 'nanos': 500000000, 'currency_code': 'EUR'}
# Type: dict

money.as_string()  # or: str(money)
# '59112.50 EUR'
# Type: string

money.as_int()  # or: int(money)
# 59112
# Type: integer

money.as_float()  # or: float(money)
# 59112.5
# Type: float
# Note that using floats may cause you to lose precision. Floats are strongly discouraged.

money.is_signed()
# False
# Type: boolean

money.is_zero()
# False
# Type: boolean

money.to_integral()
# <stockholm.Money: "59113.00 EUR">
# Type: stockholm.Money

money.amount_as_string(min_decimals=4, max_decimals=7)
# 59112.5000
# Type: string

money.amount_as_string(min_decimals=0)
# 59112.5
# Type: string

money.amount_as_string(max_decimals=0)
# 59113
# Type: string

money.to_currency(currency="SEK")
# <stockholm.Money: "59113.50 SEK">
# Type: stockholm.Money

money.as_json()
# '{"value": "59112.50 EUR", "units": 59112, "nanos": 500000000, "currency_code": "EUR"}'
# Type: string

money.as_json(keys=("amount", "currency"))
# '{"amount": "59112.50", "currency": "EUR"}'
# Type: string

money.as_protobuf()
# currency_code: "EUR"
# units: 59112
# nanos: 500000000
# Type: stockholm.protobuf.money_pb2.Money, generated from proto definitions at
# https://github.com/googleapis/googleapis/blob/master/google/type/money.proto

money.as_protobuf(proto_class=CustomMoneyProtobufMessage)
# Type: An instance of CustomMoneyProtobufMessage populated with the properties of money
```

*A simple, yet powerful way of coding with money.*

## Acknowledgements

Built with inspiration from https://github.com/carlospalol/money and https://github.com/vimeo/py-money
