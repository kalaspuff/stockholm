from __future__ import annotations

import sys
from abc import abstractmethod
from decimal import Decimal
from typing import Any, Callable, Generic, NotRequired, Required, TypeAlias, TypeVar

from .currency import CurrencyValue, MetaCurrency
from .money import Money, MoneyModel
from .rate import Number, NumericType

if sys.version_info < (3, 9):
    from typing_extensions import TypedDict  # isort: skip
else:
    from typing import TypedDict

SchemaT = TypeVar("SchemaT", bound=MoneyModel | MetaCurrency)
GetT = TypeVar("GetT")
SetT = TypeVar("SetT")


class ConvertibleTypeDescriptor(Generic[SchemaT, GetT, SetT]):
    __args__: tuple[SchemaT, GetT, SetT]

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
    amount: Required[Money | MoneyModel[Any] | int | float | Decimal | str]
    units: NotRequired[int]
    nanos: NotRequired[int]
    from_sub_units: NotRequired[bool | None]
    value: NotRequired[Money | MoneyModel[Any] | int | float | Decimal | str | None]


class NumberDictWithAmountAndEmptyCurrency(NumberDictWithAmount):
    currency_code: NotRequired[None]
    currency: NotRequired[None]


class MoneyDictWithAmountAndOptionalCurrency(NumberDictWithAmount):
    currency: NotRequired[CurrencyValue | str | None]
    currency_code: NotRequired[str | None]


class MoneyDictWithAmountAndCurrency(NumberDictWithAmount):
    currency: Required[CurrencyValue | str]
    currency_code: NotRequired[str | None]


class MoneyDictWithAmountAndCurrencyCode(NumberDictWithAmount):
    currency: NotRequired[CurrencyValue | str | None]
    currency_code: Required[str]


class NumberDictWithUnits(TypedDict):
    amount: NotRequired[Money | MoneyModel[Any] | int | float | Decimal | str | None]
    units: Required[int]
    nanos: NotRequired[int]
    from_sub_units: NotRequired[bool | None]
    value: NotRequired[Money | MoneyModel[Any] | int | float | Decimal | str | None]


class NumberDictWithUnitsAndEmptyCurrency(NumberDictWithUnits):
    currency_code: NotRequired[None]
    currency: NotRequired[None]


class MoneyDictWithUnitsAndOptionalCurrency(NumberDictWithUnits):
    currency: NotRequired[CurrencyValue | str | None]
    currency_code: NotRequired[str | None]


class MoneyDictWithUnitsAndCurrency(NumberDictWithUnits):
    currency: Required[CurrencyValue | str]
    currency_code: NotRequired[str | None]


class MoneyDictWithUnitsAndCurrencyCode(NumberDictWithUnits):
    currency: NotRequired[CurrencyValue | str | None]
    currency_code: Required[str]


class NumberDictWithNanos(TypedDict):
    amount: NotRequired[Money | MoneyModel[Any] | int | float | Decimal | str | None]
    units: NotRequired[int]
    nanos: Required[int]
    from_sub_units: NotRequired[bool | None]
    value: NotRequired[Money | MoneyModel[Any] | int | float | Decimal | str | None]


class NumberDictWithNanosAndEmptyCurrency(NumberDictWithNanos):
    currency_code: NotRequired[None]
    currency: NotRequired[None]


class MoneyDictWithNanosAndOptionalCurrency(NumberDictWithNanos):
    currency: NotRequired[CurrencyValue | str | None]
    currency_code: NotRequired[str | None]


class MoneyDictWithNanosAndCurrency(NumberDictWithNanos):
    currency: Required[CurrencyValue | str]
    currency_code: NotRequired[str | None]


class MoneyDictWithNanosAndCurrencyCode(NumberDictWithNanos):
    currency: NotRequired[CurrencyValue | str | None]
    currency_code: Required[str]


class NumberDictWithValue(TypedDict):
    amount: NotRequired[Money | MoneyModel[Any] | int | float | Decimal | str | None]
    units: NotRequired[int]
    nanos: NotRequired[int]
    from_sub_units: NotRequired[bool | None]
    value: Required[Money | MoneyModel[Any] | int | float | Decimal | str]


class NumberDictWithValueAndEmptyCurrency(NumberDictWithValue):
    currency_code: NotRequired[None]
    currency: NotRequired[None]


class MoneyDictWithValueAndOptionalCurrency(NumberDictWithValue):
    currency: NotRequired[CurrencyValue | str | None]
    currency_code: NotRequired[str | None]


class MoneyDictWithValueAndCurrency(NumberDictWithValue):
    currency: Required[CurrencyValue | str]
    currency_code: NotRequired[str | None]


class MoneyDictWithValueAndCurrencyCode(NumberDictWithValue):
    currency: NotRequired[CurrencyValue | str | None]
    currency_code: Required[str]


NumberDict = NumberDictWithAmount | NumberDictWithUnits | NumberDictWithNanos | NumberDictWithValue
NumberDictWithEmptyCurrency = (
    NumberDictWithAmountAndEmptyCurrency
    | NumberDictWithUnitsAndEmptyCurrency
    | NumberDictWithNanosAndEmptyCurrency
    | NumberDictWithValueAndEmptyCurrency
)
MoneyDictWithOptionalCurrency = (
    MoneyDictWithAmountAndOptionalCurrency
    | MoneyDictWithUnitsAndOptionalCurrency
    | MoneyDictWithNanosAndOptionalCurrency
    | MoneyDictWithValueAndOptionalCurrency
)
MoneyDictWithCurrency = (
    MoneyDictWithAmountAndCurrency
    | MoneyDictWithUnitsAndCurrency
    | MoneyDictWithNanosAndCurrency
    | MoneyDictWithValueAndCurrency
    | MoneyDictWithAmountAndCurrencyCode
    | MoneyDictWithUnitsAndCurrencyCode
    | MoneyDictWithNanosAndCurrencyCode
    | MoneyDictWithValueAndCurrencyCode
)

ConvertibleToNumberT: TypeAlias = (
    Number | NumericType[Any] | MoneyModel[Any] | NumberDict | NumberDictWithEmptyCurrency | int | float | Decimal | str
)
ConvertibleToNumber = ConvertibleTypeDescriptor[Number, Number, ConvertibleToNumberT]

ConvertibleToMoneyWithOptionalCurrencyT: TypeAlias = (
    Money | MoneyModel[Any] | NumberDict | MoneyDictWithOptionalCurrency | int | float | Decimal | str
)
ConvertibleToMoneyWithOptionalCurrency = ConvertibleTypeDescriptor[
    Money, Money, ConvertibleToMoneyWithOptionalCurrencyT
]

ConvertibleToMoneyT = ConvertibleToMoneyWithOptionalCurrencyT
ConvertibleToMoney = ConvertibleToMoneyWithOptionalCurrency

ConvertibleToMoneyWithRequiredCurrencyT: TypeAlias = Money | MoneyModel[Any] | MoneyDictWithCurrency | str
ConvertibleToMoneyWithRequiredCurrency = ConvertibleTypeDescriptor[
    Money, Money, ConvertibleToMoneyWithRequiredCurrencyT
]

ConvertibleToCurrencyCodeT: TypeAlias = CurrencyValue | str
ConvertibleToCurrency = ConvertibleTypeDescriptor[MetaCurrency, str, ConvertibleToCurrencyCodeT]
