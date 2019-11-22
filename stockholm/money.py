from functools import reduce
import re
from typing import Any, Dict, Iterable, Optional, Tuple, Union

from decimal import Decimal


__all__ = ["Money"]


class Money:
    __slots__ = ("_amount", "_currency", "_metadata")
    _amount: Decimal
    _currency: Optional[str]
    _metadata: Dict

    @classmethod
    def sort(cls, iterable: Iterable, reverse: bool = False) -> Iterable:
        return sorted(iterable, key=lambda x: x if isinstance(x, Money) else Money(x), reverse=reverse)

    @classmethod
    def sum(cls, iterable: Iterable, currency: Optional[str] = None, is_cents: Optional[bool] = None) -> "Money":
        return reduce(
            lambda v, e: v + (e if isinstance(e, Money) else Money(e, is_cents=is_cents)),
            iterable,
            Money(0, currency=currency, is_cents=is_cents),
        )

    def __init__(
        self,
        amount: Optional[Union["Money", Decimal, int, float, str, object]] = None,
        currency: Optional[str] = None,
        is_cents: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        if amount is None:
            raise Exception("Missing input values for valid monetary amount")

        if isinstance(amount, Money) and currency is None and is_cents is None:
            object.__setattr__(self, "_amount", amount.amount)
            object.__setattr__(self, "_currency", amount.currency)
            object.__setattr__(self, "_metadata", amount.metadata)
            return

        if currency is not None and not isinstance(currency, str):
            raise Exception("Invalid currency")

        output_amount = None
        output_currency = currency.strip().upper() if currency and currency.strip() else None
        output_metadata: Dict = {}

        if isinstance(amount, int) and not isinstance(amount, bool):
            if is_cents:
                output_amount = Decimal(amount) / 100
            else:
                output_amount = Decimal(amount)
        elif isinstance(amount, float):
            if is_cents:
                output_amount = Decimal(str(amount)) / 100
            else:
                output_amount = Decimal(str(amount))
        elif isinstance(amount, str) and amount.strip():
            amount = amount.strip()
            matches = re.match(r"^([-+]?[0-9.]+)[ ]+([a-zA-Z._-]+)$", amount)
            match_currency = None
            if matches:
                amount = matches.group(1).strip()
                match_currency = matches.group(2).strip().upper()
            else:
                matches = re.match(r"^([a-zA-Z._-]+)[ ]+([-+]?[0-9.]+)$", amount)
                if matches:
                    amount = matches.group(2).strip()
                    match_currency = matches.group(1).strip().upper()

            if match_currency is not None:
                if output_currency is not None and match_currency != output_currency:
                    raise Exception("Mismatching currency in input value and currency argument")
                output_currency = match_currency

            try:
                if is_cents:
                    output_amount = Decimal(amount) / 100
                else:
                    output_amount = Decimal(amount)
            except Exception:
                raise Exception("Value cannot be used as monetary amount")
        elif isinstance(amount, Money):
            if amount.currency:
                if output_currency is not None and amount.currency != output_currency:
                    raise Exception("Mismatching currency in input value and currency argument")
                output_currency = amount.currency

            if is_cents:
                output_amount = Decimal(amount.amount) / 100
            else:
                output_amount = amount.amount

            output_metadata = amount.metadata
        elif isinstance(amount, Decimal):
            if is_cents:
                output_amount = Decimal(amount) / 100
            else:
                output_amount = amount

        if output_amount is None:
            raise Exception("Missing input values for valid monetary amount")

        if output_amount > Decimal("999999999999999999.999999999"):
            raise Exception("Input amount is too high, max value is 999999999999999999.999999999")

        if output_amount < Decimal("-999999999999999999.999999999"):
            raise Exception("Input amount is too low, min value is -999999999999999999.999999999")

        if output_currency and not re.match(r"^[a-zA-Z._-]+$", output_currency):
            raise Exception("Invalid currency")

        if output_amount == 0 and str(output_amount).startswith("-"):
            output_amount = Decimal(str(output_amount)[1:])

        object.__setattr__(self, "_amount", output_amount)
        object.__setattr__(self, "_currency", output_currency)

        if "is_cents" not in output_metadata or (is_cents is not None and output_metadata["is_cents"] is not is_cents):
            output_metadata["is_cents"] = is_cents

        object.__setattr__(self, "_metadata", output_metadata)

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> Optional[str]:
        return self._currency

    @property
    def metadata(self) -> Dict:
        return self._metadata

    def _amount_tuple(self, nanos_len: int = 9) -> Tuple[str, str]:
        extended_precision = 5
        extended_precision_len = nanos_len + extended_precision
        sign, digits, exponent = self._amount.as_tuple()

        if exponent:
            units_str = "".join(map(str, digits))[:exponent] or "0"
        else:
            units_str = "".join(map(str, digits))

        nanos_str = "".join(map(str, digits))[exponent:] if exponent else ""

        nanos_str = nanos_str.rjust((-exponent), "0").ljust(extended_precision_len, "0")
        rounding_nanos = Decimal(nanos_str[nanos_len:extended_precision_len]) / Decimal(10)
        nanos_str = nanos_str[0:nanos_len]
        if rounding_nanos.quantize(Decimal(1)) * Decimal(20) >= Decimal(f"1e{extended_precision}"):
            nanos_str = str(Decimal(f"1{nanos_str}") + Decimal(1))[1:]
            if int(nanos_str) == 0:
                units_str = str(Decimal(f"1{units_str}") + Decimal(1))[1:]

        if sign:
            if int(units_str) != 0:
                units_str = f"-{units_str}"
            if int(nanos_str) != 0:
                nanos_str = f"-{nanos_str}"

        return units_str, nanos_str

    @property
    def units(self) -> int:
        units, _ = self._amount_tuple()
        return int(units)

    @property
    def nanos(self) -> int:
        _, nanos = self._amount_tuple()
        return int(nanos)

    @property
    def values(self) -> Dict:
        return {
            "units": self.units,
            "nanos": self.nanos,
            "as_string": self.amount_as_string(),
            "currency": self._currency,
        }

    def add(self, other: Any, is_cents: Optional[bool] = None) -> "Money":
        return self + Money(other, is_cents=is_cents)

    def sub(self, other: Any, is_cents: Optional[bool] = None) -> "Money":
        return self - Money(other, is_cents=is_cents)

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of monetary amounts cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of monetary amounts cannot be deleted")

    def amount_as_string(self, min_decimals: int = 2, max_decimals: int = 9) -> str:
        units, nanos = self._amount_tuple(nanos_len=max_decimals)

        decimals_value = nanos.lstrip("-")[0:max_decimals].rstrip("0")
        decimals = len(decimals_value)

        used_decimal_count = min(max(min_decimals, decimals), max_decimals)
        decimals_value = decimals_value.ljust(used_decimal_count, "0")

        if int(units) == 0 and int(nanos) < 0:
            return f"-{units}.{decimals_value}"
        return f"{units}.{decimals_value}"

    def __repr__(self) -> str:
        amount = self.amount_as_string()
        if self._currency:
            return f'<stockholm.Money: "{amount} {self._currency}">'
        return f'<stockholm.Money: "{amount}">'

    def __str__(self) -> str:
        amount = self.amount_as_string()

        if self._currency:
            return f"{amount} {self._currency}"
        return str(amount)

    def __hash__(self) -> int:
        return hash(("stockholm", self._amount, self._currency, frozenset(self._metadata)))

    def __bool__(self) -> bool:
        return bool(self._amount)

    def _convert_other(self, other: Any) -> "Money":
        if not isinstance(other, Money):
            try:
                converted_other = Money(other)
            except Exception:
                other_repr = repr(other)
                self_repr = repr(self)
                raise Exception(f"Unable to perform operations on {self_repr} with {other_repr}")
        else:
            converted_other = other

        if self._currency and converted_other._currency and self._currency != converted_other._currency:
            raise Exception("Unable to perform operations on values with differing currencies")

        return converted_other

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            try:
                converted_other = Money(other)
            except Exception:
                return False
        else:
            converted_other = other

        if self._currency and converted_other._currency and self._currency != converted_other._currency:
            if self._amount == 0 and converted_other._amount == 0:
                return True
            return False

        return self._amount == converted_other._amount

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __lt__(self, other: Any) -> bool:
        converted_other = self._convert_other(other)
        return self._amount < converted_other._amount

    def __le__(self, other: Any) -> bool:
        converted_other = self._convert_other(other)
        return self._amount <= converted_other._amount

    def __gt__(self, other: Any) -> bool:
        converted_other = self._convert_other(other)
        return self._amount > converted_other._amount

    def __ge__(self, other: Any) -> bool:
        converted_other = self._convert_other(other)
        return self._amount >= converted_other._amount

    def __add__(self, other: Any) -> "Money":
        converted_other = self._convert_other(other)
        amount = self._amount + converted_other._amount
        currency = self._currency or converted_other._currency
        return Money(amount, currency=currency)

    def __radd__(self, other: Any) -> "Money":
        return self.__add__(other)

    def __sub__(self, other: Any) -> "Money":
        converted_other = self._convert_other(other)
        amount = self._amount - converted_other._amount
        currency = self._currency or converted_other._currency
        return Money(amount, currency=currency)

    def __rsub__(self, other: Any) -> "Money":
        converted_other = self._convert_other(other)
        amount = converted_other._amount - self._amount
        currency = self._currency or converted_other._currency
        return Money(amount, currency=currency)

    def __mul__(self, other: Any) -> "Money":
        if not isinstance(other, Money):
            converted_other = self._convert_other(other)
        else:
            converted_other = other

        if converted_other._currency is not None and self._currency is not None:
            raise Exception("Unable to multiply two currency aware monetary amounts with each other")

        amount = self._amount * converted_other._amount
        currency = self._currency or converted_other._currency
        return Money(amount, currency=currency)

    def __rmul__(self, other: Any) -> "Money":
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> "Money":
        converted_other = self._convert_other(other)
        amount = self._amount / converted_other._amount

        if converted_other._currency is not None:
            return Money(amount)

        return Money(amount, currency=self._currency)

    def __floordiv__(self, other: Any) -> "Money":
        converted_other = self._convert_other(other)
        amount = self._amount // converted_other._amount

        if converted_other._currency is not None:
            return Money(amount)

        return Money(amount, currency=self._currency)

    def __mod__(self, other: Any) -> "Money":
        converted_other = self._convert_other(other)
        amount = self._amount % converted_other._amount
        currency = self._currency or converted_other._currency
        return Money(amount, currency=currency)

    def __divmod__(self, other: Any) -> Tuple["Money", "Money"]:
        converted_other = self._convert_other(other)
        quotient, remainder = divmod(self._amount, converted_other._amount)
        currency = self._currency or converted_other._currency

        if converted_other._currency is not None:
            return Money(quotient), Money(remainder, currency=currency)

        return Money(quotient, currency=currency), Money(remainder, currency=currency)

    def __pow__(self, other: Any) -> "Money":
        if not isinstance(other, Money):
            converted_other = self._convert_other(other)
        else:
            converted_other = other

        if converted_other._currency is not None:
            raise Exception("Unable to use a currency aware monetary amount as the exponential power")

        amount = self._amount ** converted_other._amount
        return Money(amount, currency=self._currency)

    def __neg__(self) -> "Money":
        return Money(-self._amount, currency=self._currency)

    def __pos__(self) -> "Money":
        return Money(+self._amount, currency=self._currency)

    def __abs__(self) -> "Money":
        return Money(abs(self._amount), currency=self._currency)

    def __int__(self) -> int:
        return int(self._amount)

    def __float__(self) -> float:
        return float(self._amount)

    def __round__(self, ndigits: int = 0) -> "Money":
        return Money(round(self._amount, ndigits), currency=self._currency)
