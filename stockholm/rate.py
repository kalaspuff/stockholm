import decimal
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, Optional, Union, cast

from .currency import CurrencyValue, DefaultCurrency, DefaultCurrencyValue
from .exceptions import ConversionError
from .money import Money, MoneyType

RoundingContext = decimal.Context(rounding=ROUND_HALF_UP)


class Rate(Money):
    _currency: None

    @classmethod
    def from_sub_units(
        cls,
        amount: Optional[Union[MoneyType, Decimal, int, float, str, object]],
        currency: Optional[Union[DefaultCurrencyValue, CurrencyValue, str]] = DefaultCurrency,
        value: Optional[Union[MoneyType, Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> "Rate":
        raise ConversionError("Rates cannot be created from sub units")

    @classmethod
    def from_dict(cls, input_dict: Dict) -> "Rate":
        return cls(**input_dict)

    def __init__(
        self,
        amount: Optional[Union[MoneyType, Decimal, Dict, int, float, str, object]] = None,
        currency: Optional[Union[DefaultCurrencyValue, CurrencyValue, str]] = DefaultCurrency,
        from_sub_units: Optional[bool] = None,
        units: Optional[int] = None,
        nanos: Optional[int] = None,
        value: Optional[Union[MoneyType, Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        if (currency is not DefaultCurrency and currency is not None) or currency_code is not None:
            raise ConversionError("Rates does not have a currency")
        if from_sub_units is not None:
            raise ConversionError("Rates cannot be created from sub units")

        cls = self.__class__.__bases__[0]
        money = cast(MoneyType, cls(amount=amount, units=units, nanos=nanos, value=value, **kwargs))

        if money._currency:
            raise ConversionError("Rates does not have a currency")

        object.__setattr__(self, "_amount", money._amount)
        object.__setattr__(self, "_currency", None)

    @property
    def currency(self) -> None:
        return None

    @property
    def currency_code(self) -> None:
        return None

    @property
    def sub_units(self) -> Decimal:
        raise ConversionError("Rates cannot be measured in sub units")

    def asdict(self) -> Dict:
        return {"value": self.value, "units": self.units, "nanos": self.nanos}

    def to_currency(self, currency: Optional[Union[CurrencyValue, str]]) -> MoneyType:  # type: ignore
        raise ConversionError("Rates does not have a currency")

    def to_sub_units(self) -> MoneyType:  # type: ignore
        raise ConversionError("Rates cannot be measured in sub units")

    def __repr__(self) -> str:
        return f'<stockholm.Rate: "{self}">'

    def __hash__(self) -> int:
        return hash(("stockholm.Rate", self._amount))


ExchangeRate = Rate
