from __future__ import annotations

import sys
from abc import abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar, Union

from .currency import BaseCurrency, CurrencyValue, MetaCurrency
from .money import Money, MoneyModel
from .rate import Number, NumericType

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, Required, TypedDict  # pragma: no cover
else:
    from typing import NotRequired, Required, TypedDict

SchemaT = TypeVar("SchemaT", bound=Union[MoneyModel, MetaCurrency])
GetT = TypeVar("GetT")
SetT = TypeVar("SetT")


class ConvertibleTypeDescriptor(Generic[SchemaT, GetT, SetT]):
    __args__: tuple[SchemaT, GetT, SetT]

    if TYPE_CHECKING:  # pragma: no cover

        @abstractmethod
        def __get__(self, instance: Any, owner: Any) -> GetT:
            ...

        def __set__(self, instance: Any, value: SetT) -> None:
            ...

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: ConvertibleTypeDescriptor[SchemaT, GetT, SetT],
        _handler: Callable,
    ) -> Any:
        return _source_type.__args__[0].__get_pydantic_core_schema__(_source_type.__args__[0], _handler)


class NumberDictWithAmount(TypedDict):
    amount: Required[Union[Money, MoneyModel[Any], int, float, Decimal, str]]
    units: NotRequired[int]
    nanos: NotRequired[int]
    from_sub_units: NotRequired[Union[bool, None]]
    value: NotRequired[Union[Money, MoneyModel[Any], int, float, Decimal, str, None]]


class NumberDictWithAmountAndEmptyCurrency(NumberDictWithAmount):
    currency_code: NotRequired[None]
    currency: NotRequired[None]


class MoneyDictWithAmountAndOptionalCurrency(NumberDictWithAmount):
    currency: NotRequired[Union[CurrencyValue, str, None]]
    currency_code: NotRequired[Union[str, None]]


class MoneyDictWithAmountAndCurrency(NumberDictWithAmount):
    currency: Required[Union[CurrencyValue, str]]
    currency_code: NotRequired[Union[str, None]]


class MoneyDictWithAmountAndCurrencyCode(NumberDictWithAmount):
    currency: NotRequired[Union[CurrencyValue, str, None]]
    currency_code: Required[str]


class NumberDictWithUnits(TypedDict):
    amount: NotRequired[Union[Money, MoneyModel[Any], int, float, Decimal, str, None]]
    units: Required[int]
    nanos: NotRequired[int]
    from_sub_units: NotRequired[Union[bool, None]]
    value: NotRequired[Union[Money, MoneyModel[Any], int, float, Decimal, str, None]]


class NumberDictWithUnitsAndEmptyCurrency(NumberDictWithUnits):
    currency_code: NotRequired[None]
    currency: NotRequired[None]


class MoneyDictWithUnitsAndOptionalCurrency(NumberDictWithUnits):
    currency: NotRequired[Union[CurrencyValue, str, None]]
    currency_code: NotRequired[Union[str, None]]


class MoneyDictWithUnitsAndCurrency(NumberDictWithUnits):
    currency: Required[Union[CurrencyValue, str]]
    currency_code: NotRequired[Union[str, None]]


class MoneyDictWithUnitsAndCurrencyCode(NumberDictWithUnits):
    currency: NotRequired[Union[CurrencyValue, str, None]]
    currency_code: Required[str]


class NumberDictWithNanos(TypedDict):
    amount: NotRequired[Union[Money, MoneyModel[Any], int, float, Decimal, str, None]]
    units: NotRequired[int]
    nanos: Required[int]
    from_sub_units: NotRequired[Union[bool, None]]
    value: NotRequired[Union[Money, MoneyModel[Any], int, float, Decimal, str, None]]


class NumberDictWithNanosAndEmptyCurrency(NumberDictWithNanos):
    currency_code: NotRequired[None]
    currency: NotRequired[None]


class MoneyDictWithNanosAndOptionalCurrency(NumberDictWithNanos):
    currency: NotRequired[Union[CurrencyValue, str, None]]
    currency_code: NotRequired[Union[str, None]]


class MoneyDictWithNanosAndCurrency(NumberDictWithNanos):
    currency: Required[Union[CurrencyValue, str]]
    currency_code: NotRequired[Union[str, None]]


class MoneyDictWithNanosAndCurrencyCode(NumberDictWithNanos):
    currency: NotRequired[Union[CurrencyValue, str, None]]
    currency_code: Required[str]


class NumberDictWithValue(TypedDict):
    amount: NotRequired[Union[Money, MoneyModel[Any], int, float, Decimal, str, None]]
    units: NotRequired[int]
    nanos: NotRequired[int]
    from_sub_units: NotRequired[Union[bool, None]]
    value: Required[Union[Money, MoneyModel[Any], int, float, Decimal, str]]


class NumberDictWithValueAndEmptyCurrency(NumberDictWithValue):
    currency_code: NotRequired[None]
    currency: NotRequired[None]


class MoneyDictWithValueAndOptionalCurrency(NumberDictWithValue):
    currency: NotRequired[Union[CurrencyValue, str, None]]
    currency_code: NotRequired[Union[str, None]]


class MoneyDictWithValueAndCurrency(NumberDictWithValue):
    currency: Required[Union[CurrencyValue, str]]
    currency_code: NotRequired[Union[str, None]]


class MoneyDictWithValueAndCurrencyCode(NumberDictWithValue):
    currency: NotRequired[Union[CurrencyValue, str, None]]
    currency_code: Required[str]


NumberDict = Union[NumberDictWithAmount, NumberDictWithUnits, NumberDictWithNanos, NumberDictWithValue]
NumberDictWithEmptyCurrency = Union[
    NumberDictWithAmountAndEmptyCurrency,
    NumberDictWithUnitsAndEmptyCurrency,
    NumberDictWithNanosAndEmptyCurrency,
    NumberDictWithValueAndEmptyCurrency,
]
MoneyDictWithOptionalCurrency = Union[
    MoneyDictWithAmountAndOptionalCurrency,
    MoneyDictWithUnitsAndOptionalCurrency,
    MoneyDictWithNanosAndOptionalCurrency,
    MoneyDictWithValueAndOptionalCurrency,
]
MoneyDictWithCurrency = Union[
    MoneyDictWithAmountAndCurrency,
    MoneyDictWithUnitsAndCurrency,
    MoneyDictWithNanosAndCurrency,
    MoneyDictWithValueAndCurrency,
    MoneyDictWithAmountAndCurrencyCode,
    MoneyDictWithUnitsAndCurrencyCode,
    MoneyDictWithNanosAndCurrencyCode,
    MoneyDictWithValueAndCurrencyCode,
]

ConvertibleToNumberT = Union[
    Number, NumericType[Any], MoneyModel[Any], NumberDict, NumberDictWithEmptyCurrency, int, float, Decimal, str
]
ConvertibleToNumber = ConvertibleTypeDescriptor[Number, Number, ConvertibleToNumberT]

ConvertibleToMoneyWithOptionalCurrencyT = Union[
    Money, MoneyModel[Any], NumberDict, MoneyDictWithOptionalCurrency, int, float, Decimal, str
]
ConvertibleToMoneyWithOptionalCurrency = ConvertibleTypeDescriptor[
    Money, Money, ConvertibleToMoneyWithOptionalCurrencyT
]

ConvertibleToMoneyT = ConvertibleToMoneyWithOptionalCurrencyT
ConvertibleToMoney = ConvertibleToMoneyWithOptionalCurrency

ConvertibleToMoneyWithRequiredCurrencyT = Union[Money, MoneyModel[Any], MoneyDictWithCurrency, str]
ConvertibleToMoneyWithRequiredCurrency = ConvertibleTypeDescriptor[
    Money, Money, ConvertibleToMoneyWithRequiredCurrencyT
]

ConvertibleToCurrencyT = Union[CurrencyValue, str]
ConvertibleToCurrency = ConvertibleTypeDescriptor[MetaCurrency, BaseCurrency, ConvertibleToCurrencyT]
