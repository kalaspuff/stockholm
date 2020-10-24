import decimal
from decimal import ROUND_HALF_UP
from typing import Any, Dict, Optional, Type, Union, cast

from .currency import BaseCurrency
from .exceptions import ConversionError
from .money import DefaultCurrency, Money, MoneyType

RoundingContext = decimal.Context(rounding=ROUND_HALF_UP)


class Number(Money):
    _currency: None

    @classmethod
    def from_sub_units(
        cls,
        amount: Optional[Union[MoneyType, decimal.Decimal, int, float, str, object]],
        currency: Optional[Union[Type[DefaultCurrency], BaseCurrency, str]] = DefaultCurrency,
        value: Optional[Union[MoneyType, decimal.Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> "Number":
        raise ConversionError("Numbers cannot be created from sub units")

    @classmethod
    def from_dict(cls, input_dict: Dict) -> "Number":
        return cls(**input_dict)

    def __init__(
        self,
        amount: Optional[Union[MoneyType, decimal.Decimal, Dict, int, float, str, object]] = None,
        currency: Optional[Union[Type[DefaultCurrency], BaseCurrency, str]] = DefaultCurrency,
        from_sub_units: Optional[bool] = None,
        units: Optional[int] = None,
        nanos: Optional[int] = None,
        value: Optional[Union[MoneyType, decimal.Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        if (currency is not DefaultCurrency and currency is not None) or currency_code is not None:
            raise ConversionError("Numbers does not have a currency")
        if from_sub_units is not None:
            raise ConversionError("Numbers cannot be created from sub units")

        super().__init__.__func__(self, amount=amount, units=units, nanos=nanos, value=value, **kwargs)
        money = cast(MoneyType, self)

        if money._currency:
            raise ConversionError("Numbers does not have a currency")

        object.__setattr__(self, "_amount", money._amount)
        object.__setattr__(self, "_currency", None)

    @property
    def currency(self) -> None:
        return None

    @property
    def currency_code(self) -> None:
        return None

    @property
    def sub_units(self) -> decimal.Decimal:
        raise ConversionError("Numbers cannot be measured in sub units")

    def asdict(self) -> Dict:
        return {"value": self.value, "units": self.units, "nanos": self.nanos}

    def to_currency(self, currency: Optional[Union[BaseCurrency, str]]) -> MoneyType:
        raise ConversionError("Numbers does not have a currency")

    def to_sub_units(self) -> MoneyType:
        raise ConversionError("Numbers cannot be measured in sub units")

    def amount_as_string(self, min_decimals: Optional[int] = None, max_decimals: Optional[int] = None) -> str:
        if min_decimals is None:
            min_decimals = 0
        return super().amount_as_string(min_decimals, max_decimals)

    def __repr__(self) -> str:
        return f'<stockholm.Number: "{self}">'

    def __hash__(self) -> int:
        return hash(("stockholm.Number", self._amount))


Decimal = Number
