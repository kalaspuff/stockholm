# `stockholm` — `Money` for Python 3
[![pypi](https://badge.fury.io/py/stockholm.svg)](https://pypi.python.org/pypi/stockholm/)
[![MIT License](https://img.shields.io/github/license/kalaspuff/stockholm.svg)](https://github.com/kalaspuff/stockholm/blob/master/LICENSE)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Library for formatting and performing arithmetic and comparison operations on monetary amounts. Also with support for currency handling, exchange and network transport structure generation as well as parsing.

An up to date human friendly and flexible approach for development with any kind of monetary amounts.

At its bone a `Money` class for Python 3.x. This is a library to be used by backend and frontend API coders of fintech companies, web merchants and subscription services. A simple, yet powerful way of coding with money.

The `stockholm.Money` object has full arithmetic support together with `int`, `float`, `Decimal`, other `Money` objects as well as `string`. The `stockholm.Money` object also supports complex string formatting functionality for easy debugging and a clean coding pattern.

### Installation with `pip`
```
$ pip install stockholm
```

### Examples
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

*Advanced string formatting functionality*
```python
from stockholm import Money

jpy_money = Money(1352953, "JPY")
exchange_rate = Money("0.08861326")
sek_money = Money(jpy_money * exchange_rate, "SEK")

print(f"I have {jpy_money:,.0m} which equals around {sek_money:,.2m}")
print(f"The exchange rate is {exchange_rate} ({jpy_money:c} -> {sek_money:c})")
# I have 1,352,953 JPY which equals around 119,889.58 SEK
# The exchange rate is 0.08861326 (JPY -> SEK)

print(f"{jpy_money:.0f}")
# 1352953

print(f"{sek_money:.2f}")
# 119889.58

print(f"{sek_money:.1f}")
# 119889.6

print(f"{sek_money:.0f}")
# 119890
```

*Flexible ways for assigning values to a monetary amount*
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
# <stockholm.Money: "1666.666666667">

money = Money("0.30285471")
Money(money, currency="BTC")
# <stockholm.Money: "0.30285471 BTC">

cents_as_str = "471100"
Money(cents_as_str, currency="USD", is_cents=True)
# <stockholm.Money: "4711.00 USD">
```

*Adding several monetary amounts from a list*
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

### Acknowledgements
Built with inspiration from https://github.com/carlospalol/money and https://github.com/vimeo/py-money
