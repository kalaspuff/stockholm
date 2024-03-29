# Changelog

## [0.5.7] - 2023-11-23

* `Money` objects can be used in Pydantic (`Pydantic>=2.2` supported) models and used with Pydantic's JSON serialization and validation – the same goes for `Number` and `Currency` objects as well. See examples below.

  Previously validation of these types required the Pydantic config option `arbitrary_types_allowed` and JSON serialization with `model_dump_json()` resulted in an exception. With these updates there's no need for `arbitrary_types_allowed` and pydantic model's using `Money` fields can use JSON serialization+deserialization natively.
* It's also possible to use the coercible types as Pydantic field type – mainly suited for experimentation and early development. These types will automatically coerce input into `Money`, `Number` or `Currency` objects.
  * `stockholm.types.ConvertibleToMoney`
  * `stockholm.types.ConvertibleToMoneyWithRequiredCurrency`
  * `stockholm.types.ConvertibleToNumber`
  * `stockholm.types.ConvertibleToCurrency`
* Dropped support for Python 3.7.

---

#### Example of using `Money` fields in Pydantic models

```python
from pydantic import BaseModel
from stockholm import Money

class Transaction(BaseModel):
    reference: str
    amount: Money

transaction = Transaction(reference="abc123", amount=Money("100.00", "SEK"))
# Transaction(reference='abc123', amount=<stockholm.Money: "100.00 SEK">)

json_data = transaction.model_dump_json()
# '{"reference":"abc123","amount":{"value":"100.00 SEK","units":100,"nanos":0,"currency_code":"SEK"}}'

Transaction.model_validate_json(json_data)
# Transaction(reference='abc123', amount=<stockholm.Money: "100.00 SEK">)
```

#### Example of using coercible fields such as `ConvertibleToMoney` in Pydantic models

```python
from pydantic import BaseModel
from stockholm import Money
from stockholm.types import ConvertibleToMoney

class ExampleModel(BaseModel):
    amount: ConvertibleToMoney

example = ExampleModel(amount="4711.50 USD")
# ExampleModel(amount=<stockholm.Money: "4711.50 USD">)

example.model_dump_json()
# '{"amount":{"value":"4711.50 USD","units":4711,"nanos":500000000,"currency_code":"USD"}}'
```

Note that it's generally recommended to opt for the more strict types (`stockholm.Money`, `stockholm.Number` and `stockholm.Currency`) when possible.

---

## [0.5.6] - 2023-08-15

* Added so that `Money`, `Number` and `Rate` objects can now be copied using the `copy.copy()` and `copy.deepcopy()` functions.
* Python 3.12 added to test matrix and trove classifiers.
* Fixes some type hints that previously would show as `Unknown` in some LSPs.

---

## [0.5.5] - 2022-12-07

* Additional support to parse input values from third parties, data models, etc.
* Primarily load protobuf message class from `google.type.money_pb2` before falling back to the included class in `stockholm.protobuf.money_pb2`.
* Added `SLE` and `VED` to `stockholm.currency`.

---

## [0.5.4] - 2022-11-22

* The `money.asdict()` function can now be called with an optional `keys` argument, which can be used to specify a tuple of keys which shuld be used in the returned dict.
* A `Number` class has been added, which can be used to differentiate between monetary values and values that doesn't hold a currency – `stockholm.Number`. Like `Rate` objects, the `Number` objects cannot be instantiated with a currency or currency code.
* Added additional documentation and examples to the README.

---

The default behaviour for calling `money.asdict()` without arguments has not changed. `money.asdict()` is equivalent to `money.asdict(keys=("value", "units", "nanos", "currency_code"))`.

Values to use in the `keys` tuple for `stockholm.Money` objects are any combination of the following:

| key | description | return type | example |
| :-- | :---------- | :---------- | -------: |
| `value` | amount + currency code | `str` | `"9001.50 USD"`
| `units` | units of the amount | `int` | `9001` |
| `nanos` | number of nano units of the amount | `int` | `500000000` |
| `currency_code` | currency code if available | `str \| None` | `"USD"` |
| `currency` | currency code if available | `str \| None` | `"USD"` |
| `amount` | the monetary amount (excl. currency code) | `str` | `"9001.50"` |

Code examples:

```python
from stockholm import Money

Money("4711 USD").asdict(keys=("value", "units", "nanos", "currency_code"))
# {'value': '4711.00 USD', 'units': 4711, 'nanos': 0, 'currency_code': 'USD'}

Money("4711 USD").asdict(keys=("amount", "currency"))
# {'amount': '4711.00', 'currency': 'USD'}

Money(nanos=10).asdict(keys=("value", "currency", "units", "nanos"))
# {'value': '0.00000001', 'currency': None, 'units': 0, 'nanos': 10}
```

---

## [0.5.3] - 2022-10-25

* Python 3.11 added to test matrix and trove classifiers to officially claim support.

---

## [0.5.2] - 2022-10-14

* Adds support for the `protobuf` Python bindings versioned 4.x.x.
* Fixes an issue with the `__hash__` method on `Currency` objects which affected currencies with an `interchangeable_with` value, such as `CNY` (+ `CNH` / `RMB`), `ILS` (+ `NIS`), `TWD` (+ `NTD`). [Thanks @th-ad]

---

## [0.5.1] - 2022-02-28

* Python 3.10 added to test matrix and trove classifiers to officially claim support.

---

## [0.5.0] - 2021-06-30

* Major updates to improve type hints and intellisense within editors.
* Reworked the currency classes to utilize the metaclass in a better way.
* Additional updates to ease development working with Protocol Buffers and monetary amounts (mostly related to better type hint annotations which gives a better developer experience).
* Updates to the readme with additional examples.
* Dropped support for Python 3.6.

---

## [0.4.4] - 2020-11-09

* Python 3.9 supported.
* Minor type annotation fixes.

---

## [0.4.3] - 2020-09-28

* Fixes an issue that caused a monetary amount without currency to get a `"None"` string instead of an empty string as value to `currency_code` when creating a protobuf message using the `.as_protobuf()` method.

---

## [0.4.2] - 2020-06-29

* Added support for conversion to and from Protocol Buffers using the new `Money.from_protobuf` or `money.as_protobuf` functions. By default using the [`google.type.Money`](https://github.com/googleapis/googleapis/blob/master/google/type/money.proto) protobuf definition.
* Instantiation of monetary object by passing JSON data and the possibility to get a JSON string based on a monetary amount object.
* Added documentation. Mostly regarding the use and examples about Protocol Buffers, but also a whole new section about the properties that are available on the `stockholm.Money` object.

---

## [0.4.1] - 2020-06-26

* Updated versions for test suite (`flake8`, `pytest`, `mypy`, among others) and then corrected a newly found type hinting issue tracked down by the updated versions.
* Added target-versions of the supported Python versions for `black` to not accidentally break any backwards compatibility.
* Fixes default decimal digit formatting of the Ugandan shilling (*currency code **UGX***). [Thanks @tritas]

---

## [0.4.0] - 2019-12-07

* Added a sub type of `Money` which is named `Rate`, which mostly works the same way but doesn't support currencies. In many applications monetary values can be multiplied with rates (the *rate* can for example be the units of an item on an invoice, where the sum of the item row would be the item price multiplied with the rate). The `Rate` sub type is merely for differentiating monetary values (which fully supports currencies) from the simpler rate type.
* Updated type hinting and object creation methods to work with inheritance.

---

## [0.3.7] - 2019-11-28

* Monetary amounts can also be exported to `dict` as well as created with `dict` value inputs, which can be great to for example transport a monetary value in JSON.
* To return a dict from a `stockholm.Money` object it can either be casted to `dict` (`dict(money)`) or by using `money.asdict()`.
* Monetary amounts can also be created using dict input either by using `Money.from_dict(input_dict)` or by calling the constructor directly with `dict` input such as `Money(dict_input)`.

---

## [0.3.6] - 2019-11-28

* Project documentation improvements.
* Removed debug output on currency imports.

---

## [0.3.5] - 2019-11-28

* Added money() method to currency objects. For example `stockholm.Currency.EUR.money(100)` would equal `stockholm.Money(100, stockholm.Currency.EUR)`.
* Prevents currency objects to create new currency objects by using them as object constructors.

---

## [0.3.4] - 2019-11-28

* Added shortcut to `round(self, 0)` as the method `to_integral` which also returns a `Money` object.
* Added `currency_code` as a property which outputs the currency in string format.

---

## [0.3.3] - 2019-11-27

* Added `sub_units` property of money objects for easy conversion to and from sub_units.

---

## [0.3.2] - 2019-11-27

* Updated README with examples about `units` and `nanos` properties.
* Added `get_currency(ticker)` method available directly from root package, to make it importable with `from stockholm import get_currency`.

---

## [0.3.1] - 2019-11-27

* Adds method `to_sub_units()` on monetary amounts which for most currencies multiplies the value with 100, but for example for `stockholm.currency.JPY` wouldn't change the value at all.
* Adds method `to_currency(currency)` (and shorted `to(currency)`) on monetary amounts which just changes the currency of the monetary amount without any kind of changes to the amount itself.

---

## [0.3.0] - 2019-11-27

* `Money.from_sub_units(amount, currency)` method is a classmethod which does the same thing as `Money(amount, currency, from_sub_units=True)`. For example a `100` subunits of `stockholm.Currency.SEK` would result in a monetary amount of `1.00 SEK`, while 100 subunits of `stockholm.Currency.JPY` would result in `100 JPY`.

---

## [0.2.2] - 2019-11-27

* Replaces `is_cents` with `from_sub_units` which is aware of number of digits in a `BaseCurrency`.

---

## [0.2.1] - 2019-11-27

* Added support for custom currency types with non-uppercase ticker symbols.

---

## [0.2.0] - 2019-11-27

* Restructured currency to also be able to fetch currencies directly on `stockholm.Currency`

---

## [0.1.1] - 2019-11-26

* Added `get_currency(currency)` method to `stockholm.currency` which returns a currency type that includes metadata about formatting and the default minimum decimals digits, etc.

---

## [0.1.0] - 2019-11-25

### Initial release

* First release with support for monetary amounts using currency types.
* All ISO 4217 currency types available in `stockholm.currency`. All currencies uses official values for the default minimum decimal digit count.
