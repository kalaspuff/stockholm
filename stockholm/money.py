from functools import reduce
import re
from typing import Any, Iterable, Optional, Tuple, Union

from decimal import Decimal, ROUND_HALF_UP

from .exceptions import CurrencyMismatchError, ConversionError, InvalidOperandError


__all__ = ["Money"]

DEFAULT_MIN_DECIMALS = 2
DEFAULT_MAX_DECIMALS = 9
MAX_DECIMALS = 9
UNITS_MAX_LENGTH = 18
NANOS_LENGTH = 9

HIGHEST_SUPPORTED_AMOUNT = "999999999999999999.999999999"
LOWEST_SUPPORTED_AMOUNT = "-999999999999999999.999999999"


class Money:
    __slots__ = ("_amount", "_currency")
    _amount: Decimal
    _currency: Optional[str]

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

    @classmethod
    def _is_unknown_amount_type(cls, amount: Optional[Union["Money", Decimal, int, float, str, object]]) -> bool:
        return not any(map(lambda type_: isinstance(amount, type_), (Money, Decimal, int, bool, float, str)))

    def __init__(
        self,
        amount: Optional[Union["Money", Decimal, int, float, str, object]] = None,
        currency: Optional[str] = None,
        is_cents: Optional[bool] = None,
        units: Optional[int] = None,
        nanos: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        validate_amounts = []

        if units is not None or nanos is not None:
            try:
                units = units or 0
                nanos = nanos or 0
                if (units > 0 and nanos < 0) or (units < 0 and nanos > 0):
                    raise ValueError
                units_str = str(units).lstrip("-")
                nanos_str = str(nanos).lstrip("-").rjust(NANOS_LENGTH, "0")
                if len(units_str) > UNITS_MAX_LENGTH:
                    raise ValueError
                if len(nanos_str) != NANOS_LENGTH:
                    raise ValueError
                sign = "-" if nanos < 0 or units < 0 else ""
                units_amount = Decimal(f"{sign}{units_str}.{nanos_str}")
                if amount is None:
                    amount = units_amount
                else:
                    validate_amounts.append(units_amount)
            except Exception:
                raise ConversionError("Invalid values for units and nanos")

        if amount is None:
            raise ConversionError("Missing input values for monetary amount")

        if isinstance(amount, Money) and currency is None and is_cents is None and units is None and nanos is None:
            object.__setattr__(self, "_amount", amount._amount)
            object.__setattr__(self, "_currency", amount._currency)
            return

        if currency is not None and not isinstance(currency, str):
            raise ConversionError("Invalid currency value")

        output_amount = None
        output_currency = currency.strip().upper() if currency and currency.strip() else None

        if Money._is_unknown_amount_type(amount):
            try:
                match_amount = getattr(amount, "amount")
                if match_amount is None or Money._is_unknown_amount_type(match_amount):
                    raise AttributeError

                match_currency = None
                try:
                    match_currency = getattr(amount, "currency")
                    if not match_currency:
                        raise AttributeError
                except AttributeError:
                    matches = re.match(r"^(?:[-+]?[0-9.]+)[ ]+([a-zA-Z]+)$", str(amount))
                    if not matches:
                        matches = re.match(r"^([a-zA-Z]+)[ ]+(?:[-+]?[0-9.]+)$", str(amount))
                    if matches:
                        match_currency = matches.group(1)

                if match_currency is not None:
                    match_currency = match_currency.strip().upper()
                    if output_currency is not None and match_currency != output_currency:
                        raise ConversionError("Mismatching currency in input value and currency argument")
                    output_currency = match_currency

                amount = match_amount
            except AttributeError:
                amount = str(amount)

        if amount is not None and isinstance(amount, int) and not isinstance(amount, bool):
            output_amount = Decimal(amount)
        elif amount is not None and isinstance(amount, float):
            output_amount = Decimal(str(amount))
        elif amount is not None and isinstance(amount, str) and amount.strip():
            amount = amount.strip()
            match_currency = None

            matches = re.match(r"^(?P<amount>[-+]?[0-9.]+)[ ]+(?P<currency>[a-zA-Z]+)$", amount)
            if not matches:
                matches = re.match(r"^(?P<currency>[a-zA-Z]+)[ ]+(?P<amount>[-+]?[0-9.]+)$", amount)
            if matches:
                amount = matches.group("amount").strip()
                match_currency = matches.group("currency").strip().upper()

            if match_currency is not None:
                if output_currency is not None and match_currency != output_currency:
                    raise ConversionError("Mismatching currency in input value and currency argument")
                output_currency = match_currency

            try:
                output_amount = Decimal(amount)
            except Exception:
                raise ConversionError("Value cannot be used as monetary amount")
        elif amount is not None and isinstance(amount, Money):
            if amount.currency:
                if output_currency is not None and amount.currency != output_currency:
                    raise ConversionError("Mismatching currency in input value and currency argument")
                output_currency = amount.currency

            output_amount = amount._amount
        elif amount is not None and isinstance(amount, Decimal):
            output_amount = amount

        if output_amount is None:
            raise ConversionError("Missing input values for monetary amount")

        if output_amount.is_infinite():
            raise ConversionError("Monetary amounts cannot be infinite")

        if output_amount.is_nan():
            raise ConversionError("Input amount is not a number")

        if is_cents:
            output_amount = output_amount / 100

        if output_amount > Decimal(HIGHEST_SUPPORTED_AMOUNT):
            raise ConversionError(f"Input amount is too high, max value is {HIGHEST_SUPPORTED_AMOUNT}")

        if output_amount < Decimal(LOWEST_SUPPORTED_AMOUNT):
            raise ConversionError(f"Input amount is too low, min value is {LOWEST_SUPPORTED_AMOUNT}")

        if output_currency and not re.match(r"^[a-zA-Z]+$", output_currency):
            raise ConversionError("Invalid currency")

        if output_amount == 0 and str(output_amount).startswith("-"):
            output_amount = Decimal(0)

        if any([output_amount != a for a in validate_amounts]):
            raise ConversionError("Input arguments does not match")

        object.__setattr__(self, "_amount", output_amount)
        object.__setattr__(self, "_currency", output_currency)

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> Optional[str]:
        return self._currency

    @property
    def _amount_tuple(self) -> Tuple[str, str]:
        amount = self._amount.quantize(Decimal(f"1e-{NANOS_LENGTH}"), ROUND_HALF_UP)
        sign, digits, exponent = amount.as_tuple()

        units_str = "".join(map(str, digits))[:exponent] or "0"

        nanos_str = "".join(map(str, digits))[exponent:]
        nanos_str = nanos_str.rjust((-exponent), "0").ljust(NANOS_LENGTH, "0")[0:NANOS_LENGTH]

        if sign and int(units_str):
            units_str = f"-{units_str}"
        if sign and int(nanos_str):
            nanos_str = f"-{nanos_str}"

        return units_str, nanos_str

    @property
    def units(self) -> int:
        units, _ = self._amount_tuple
        return int(units)

    @property
    def nanos(self) -> int:
        _, nanos = self._amount_tuple
        return int(nanos)

    def as_string(self) -> str:
        return str(self)

    def as_str(self) -> str:
        return self.as_string()

    def as_decimal(self) -> Decimal:
        return self._amount

    def add(self, other: Any, is_cents: Optional[bool] = None) -> "Money":
        return self + Money(other, is_cents=is_cents)

    def sub(self, other: Any, is_cents: Optional[bool] = None) -> "Money":
        return self - Money(other, is_cents=is_cents)

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of monetary amounts cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of monetary amounts cannot be deleted")

    def amount_as_string(
        self, min_decimals: int = DEFAULT_MIN_DECIMALS, max_decimals: int = DEFAULT_MAX_DECIMALS
    ) -> str:
        units, nanos = self._amount_tuple

        max_decimals = min(max_decimals, MAX_DECIMALS)
        min_decimals = min(min_decimals, max_decimals)

        decimals_value = nanos.lstrip("-")[0:max_decimals].rstrip("0")
        decimals = len(decimals_value)

        used_decimal_count = min(max(min_decimals, decimals), max_decimals)
        decimals_value = decimals_value.ljust(used_decimal_count, "0")

        if not int(units) and int(nanos) < 0:
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
        return hash(("stockholm.Money", self._amount, self._currency))

    def __bool__(self) -> bool:
        return bool(self._amount)

    def _convert_other(self, other: Any) -> "Money":
        if not isinstance(other, Money):
            try:
                converted_other = Money(other)
            except ConversionError:
                other_repr = repr(other)
                self_repr = repr(self)
                raise InvalidOperandError(f"Unable to perform operations on {self_repr} with {other_repr}")
        else:
            converted_other = other

        if self._currency and converted_other._currency and self._currency != converted_other._currency:
            raise CurrencyMismatchError("Unable to perform operations on values with differing currencies")

        return converted_other

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            try:
                converted_other = Money(other)
            except ConversionError:
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
            raise InvalidOperandError("Unable to multiply two monetary amounts with each other")

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
            raise InvalidOperandError("Unable to use a monetary amount as an exponent")

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
