import decimal
import json
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from .compat import CurrencyValue
from .currency import DefaultCurrency, DefaultCurrencyValue
from .exceptions import ConversionError
from .money import Money, MoneyModel, MoneyType

DEFAULT_MIN_DECIMALS = 0
DEFAULT_MAX_DECIMALS = 9

RoundingContext = decimal.Context(rounding=ROUND_HALF_UP)


class NumericType(MoneyModel[MoneyType]):
    _currency: None

    @classmethod
    def from_sub_units(
        cls,
        amount: Optional[Union[MoneyType, MoneyModel[Any], Decimal, int, float, str, object]],
        currency: Optional[Union[DefaultCurrencyValue, CurrencyValue, str]] = DefaultCurrency,
        value: Optional[Union[MoneyType, MoneyModel[Any], Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> MoneyType:
        raise ConversionError("Rates and numbers cannot be created from sub units")

    def __init__(
        self,
        amount: Optional[Union[MoneyType, MoneyModel[Any], Decimal, Dict, int, float, str, object]] = None,
        units: Optional[int] = None,
        nanos: Optional[int] = None,
        value: Optional[Union[MoneyType, MoneyModel[Any], Decimal, int, float, str]] = None,
        **kwargs: Any,
    ) -> None:
        currency = kwargs.get("currency", DefaultCurrency)
        currency_code = kwargs.get("currency_code")
        from_sub_units = kwargs.get("from_sub_units")
        if (currency is not DefaultCurrency and currency is not None) or currency_code is not None:
            raise ConversionError("Rates and numbers does not have a currency")
        if from_sub_units is not None:
            raise ConversionError("Rates and numbers cannot be created from sub units")

        cls = self.__class__.__bases__[0]
        money = cast(MoneyType, cls(amount=amount, units=units, nanos=nanos, value=value, **kwargs))

        if money._currency:
            raise ConversionError("Rates and numbers does not have a currency")

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
        raise ConversionError("Rates and numbers cannot be measured in sub units")

    def asdict(
        self, keys: Union[List[str], Tuple[str, ...]] = ("value", "units", "nanos")
    ) -> Dict[str, Optional[Union[str, int]]]:
        output: Dict[str, Optional[Union[str, int]]] = {}
        for key in keys:
            if key in ("value", "amount"):
                output[key] = self.value
            elif key == "units":
                output[key] = self.units
            elif key == "nanos":
                output[key] = self.nanos

        return output

    def as_dict(
        self, keys: Union[List[str], Tuple[str, ...]] = ("value", "units", "nanos")
    ) -> Dict[str, Optional[Union[str, int]]]:
        return self.asdict(keys=keys)

    def as_json(self, keys: Union[List[str], Tuple[str, ...]] = ("value", "units", "nanos")) -> str:
        return json.dumps(self.asdict(keys=keys))

    def json(self, keys: Union[List[str], Tuple[str, ...]] = ("value", "units", "nanos")) -> str:
        return self.as_json(keys=keys)

    def amount_as_string(self, min_decimals: Optional[int] = None, max_decimals: Optional[int] = None) -> str:
        if min_decimals is None:
            min_decimals = DEFAULT_MIN_DECIMALS
        if max_decimals is None:
            max_decimals = DEFAULT_MAX_DECIMALS
        return super().amount_as_string(min_decimals=min_decimals, max_decimals=max_decimals)

    def to_currency(self, currency: Optional[Union[CurrencyValue, str]]) -> Money:
        return Money(self, currency=currency)

    def to_sub_units(self) -> MoneyType:
        raise ConversionError("Rates and numbers cannot be measured in sub units")

    def __repr__(self) -> str:
        return f'<stockholm.{self.__class__.__name__}: "{self}">'

    def __hash__(self) -> int:
        return hash((f"stockholm.{self.__class__.__name__}", self._amount))


class Rate(NumericType["Rate"]):
    pass


ExchangeRate = Rate


class Number(NumericType["Number"]):
    pass
