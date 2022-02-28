from __future__ import annotations

import decimal
import json
import re
from decimal import ROUND_HALF_UP, Decimal
from functools import reduce
from typing import Any, Dict, Generic, Iterable, List, Optional, Tuple, Type, TypeVar, Union, cast

from .currency import BaseCurrencyType, CurrencyValue, DefaultCurrency, DefaultCurrencyValue
from .exceptions import ConversionError, CurrencyMismatchError, InvalidOperandError
from .protobuf import GenericProtobufMessage, MoneyProtobufMessage

__all__ = ["Money"]

DEFAULT_MIN_DECIMALS = 2
DEFAULT_MAX_DECIMALS = 9
UNITS_MAX_LENGTH = 18
NANOS_LENGTH = 9

HIGHEST_SUPPORTED_AMOUNT = "999999999999999999.999999999"
LOWEST_SUPPORTED_AMOUNT = "-999999999999999999.999999999"

RoundingContext = decimal.Context(rounding=ROUND_HALF_UP)

_parse_format_specifier_regex = re.compile(
    r"""\A
(?:
   (?P<fill>.)?
   (?P<align>[<>=^])
)?
(?P<sign>[-+ ])?
(?P<zeropad>0)?
(?P<minimumwidth>(?!0)\d+)?
(?P<thousands_sep>[,_])?
(?:\.(?P<precision>0|(?!0)\d+))?
(?P<type>[cCdfFmMs])?
\Z
""",
    re.VERBOSE,
)


MoneyType = TypeVar("MoneyType", bound="MoneyModel")
ProtobufMessageType = TypeVar("ProtobufMessageType", bound=GenericProtobufMessage)


class MoneyModel(Generic[MoneyType]):
    __slots__ = ("_amount", "_currency")
    _amount: Decimal
    _currency: Optional[Union[CurrencyValue, str]]

    @classmethod
    def sort(cls, iterable: Iterable, reverse: bool = False) -> Iterable:
        return sorted(iterable, key=lambda x: x if isinstance(x, cls) else cls(x), reverse=reverse)

    @classmethod
    def sum(
        cls,
        iterable: Iterable,
        currency: Optional[Union[DefaultCurrencyValue, CurrencyValue, str]] = DefaultCurrency,
        currency_code: Optional[str] = None,
        from_sub_units: Optional[bool] = None,
        **kwargs: Any,
    ) -> MoneyType:
        return cast(
            MoneyType,
            reduce(
                lambda v, e: v + (e if isinstance(e, cls) else cls(e, from_sub_units=from_sub_units)),
                iterable,
                cls(0, currency=currency, currency_code=currency_code, from_sub_units=from_sub_units),
            ),
        )

    @classmethod
    def _is_unknown_amount_type(cls, amount: Optional[Union[MoneyType, Decimal, int, float, str, object]]) -> bool:
        return not any(map(lambda type_: isinstance(amount, type_), (Money, Decimal, int, bool, float, str)))

    @classmethod
    def from_sub_units(
        cls: Type[MoneyType],
        amount: Optional[Union[MoneyType, Decimal, int, float, str, object]],
        currency: Optional[Union[DefaultCurrencyValue, CurrencyValue, str]] = DefaultCurrency,
        value: Optional[Union[MoneyType, Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> MoneyType:
        return cls(amount=amount, currency=currency, from_sub_units=True, value=value, **kwargs)

    @classmethod
    def from_dict(cls: Type[MoneyType], input_dict: Dict) -> MoneyType:
        return cls(**input_dict)

    @classmethod
    def from_json(cls: Type[MoneyType], input_value: Union[str, bytes]) -> MoneyType:
        return cls(**json.loads(input_value))

    @classmethod
    def from_protobuf(
        cls: Type[MoneyType],
        input_value: Union[str, bytes, object],
        proto_class: Type[GenericProtobufMessage] = MoneyProtobufMessage,
    ) -> MoneyType:
        if input_value is not None and isinstance(input_value, bytes):
            input_value = proto_class.FromString(input_value)

        return cls(
            **{
                k: getattr(input_value, k)
                for k in (
                    "value",
                    "units",
                    "nanos",
                    "amount",
                    "currency",
                    "currency_code",
                    "from_sub_units",
                )
                if hasattr(input_value, k)
            }
        )

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
                new_decimal = Decimal(f"{sign}{units_str}.{nanos_str}")
                if amount is None:
                    amount = new_decimal
                else:
                    validate_amounts.append(new_decimal)
            except Exception:
                raise ConversionError("Invalid values for 'units' and 'nanos'")

        if value is not None:
            try:
                new_amount = cast(MoneyType, self.__class__(value))
                if currency_code is None:
                    currency_code = new_amount.currency_code
                elif new_amount.currency_code and new_amount.currency_code != currency_code:
                    raise ConversionError("Invalid value for 'value'")
                if amount is None:
                    amount = new_amount
                else:
                    validate_amounts.append(new_amount.amount)
            except Exception:
                raise ConversionError("Invalid value for 'value'")

        if amount is not None and isinstance(amount, Dict):
            amount = self.__class__.from_dict(amount)

        if amount is None:
            raise ConversionError("Missing input values for monetary amount")

        if currency is DefaultCurrency and currency_code:
            if not isinstance(currency_code, str):
                raise ConversionError("Invalid 'currency_code' value, must be string")
            currency = str(currency_code)
        elif currency is not DefaultCurrency and currency_code and str(currency) != str(currency_code):
            raise ConversionError("Invalid 'currency' value, does not match 'currency_code'")

        if (
            isinstance(amount, Money)
            and currency is DefaultCurrency
            and from_sub_units is None
            and units is None
            and nanos is None
        ):
            object.__setattr__(self, "_amount", amount._amount)
            object.__setattr__(self, "_currency", amount._currency)
            return

        if (
            currency is not DefaultCurrency
            and not isinstance(currency, str)
            and not isinstance(currency, BaseCurrencyType)
            and currency is not None
        ):
            raise ConversionError("Invalid 'currency' value")

        output_amount = None
        output_currency: Optional[Union[CurrencyValue, str]] = None
        if currency is not DefaultCurrency:
            if isinstance(currency, BaseCurrencyType):
                output_currency = currency
            else:
                output_currency = str(currency or "").strip() or None
                output_currency = (
                    output_currency.upper() if output_currency and len(output_currency) == 3 else output_currency
                )

        if amount is not None and (
            (isinstance(amount, str) and len(amount) > 1 and amount[0] == "{")
            or (isinstance(amount, bytes) and len(amount) > 1 and amount[0] == 123)
        ):
            try:
                amount = str(self.__class__.from_dict(json.loads(amount)))
            except Exception:
                pass

        if amount is not None and isinstance(amount, bytes):
            try:
                amount = MoneyProtobufMessage.FromString(amount)
            except Exception:
                pass

        if amount is not None and isinstance(amount, GenericProtobufMessage):
            amount = str(
                self.__class__.from_dict(
                    {
                        k: getattr(amount, k)
                        for k in (
                            "value",
                            "units",
                            "nanos",
                            "amount",
                            "currency",
                            "currency_code",
                            "from_sub_units",
                        )
                        if hasattr(amount, k)
                    }
                )
            )

        if Money._is_unknown_amount_type(amount):
            try:
                match_amount = getattr(amount, "amount")
                match_amount = (match_amount()) if match_amount and callable(match_amount) else match_amount
                if match_amount is None or Money._is_unknown_amount_type(match_amount):
                    raise AttributeError

                match_currency = None
                try:
                    match_currency = getattr(amount, "currency")
                    match_currency = (
                        (match_currency()) if match_currency and callable(match_currency) else match_currency
                    )
                    if not match_currency:
                        raise AttributeError
                except AttributeError:
                    matches = re.match(r"^(?:[-+]?[0-9.]+)[ ]+([a-zA-Z]+)$", str(amount))
                    if not matches:
                        matches = re.match(r"^([a-zA-Z]+)[ ]+(?:[-+]?[0-9.]+)$", str(amount))
                    if matches:
                        match_currency = matches.group(1)

                if match_currency is not None:
                    match_currency = str(match_currency).strip()
                    match_currency = (
                        match_currency.upper()
                        if match_currency and isinstance(match_currency, str) and len(match_currency) == 3
                        else match_currency
                    )
                    if output_currency is not None and match_currency != output_currency:
                        raise ConversionError("Mismatching currency in input value and 'currency' argument")
                    output_currency = (
                        output_currency if isinstance(output_currency, BaseCurrencyType) else match_currency
                    )

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
                match_currency = matches.group("currency").strip()
                match_currency = (
                    match_currency.upper()
                    if match_currency and isinstance(match_currency, str) and len(match_currency) == 3
                    else match_currency
                )

            if match_currency is not None:
                if output_currency is not None and match_currency != output_currency:
                    raise ConversionError("Mismatching currency in input value and 'currency' argument")
                output_currency = output_currency if isinstance(output_currency, BaseCurrencyType) else match_currency

            try:
                output_amount = Decimal(amount)
            except Exception:
                raise ConversionError("Input value cannot be used as monetary amount")
        elif amount is not None and isinstance(amount, Money):
            if amount.currency and not output_currency and currency is DefaultCurrency:
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

        if from_sub_units:
            if output_currency and isinstance(output_currency, BaseCurrencyType):
                if output_currency.decimal_digits != 0:
                    output_amount = output_amount / Decimal(pow(10, output_currency.decimal_digits))
            else:
                output_amount = output_amount / 100

        if output_amount > Decimal(HIGHEST_SUPPORTED_AMOUNT):
            raise ConversionError(f"Input amount is too high, max value is {HIGHEST_SUPPORTED_AMOUNT}")

        if output_amount < Decimal(LOWEST_SUPPORTED_AMOUNT):
            raise ConversionError(f"Input amount is too low, min value is {LOWEST_SUPPORTED_AMOUNT}")

        if output_currency and not re.match(r"^[A-Za-z]+$", str(output_currency)):
            raise ConversionError("Invalid 'currency' or 'currency_code'")

        if output_amount == 0 and output_amount.is_signed():
            output_amount = Decimal(0)

        if any([output_amount != a for a in validate_amounts]):
            raise ConversionError("Values in input arguments does not match")

        object.__setattr__(self, "_amount", output_amount)
        object.__setattr__(self, "_currency", output_currency)

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> Optional[Union[CurrencyValue, str]]:
        return self._currency

    @property
    def currency_code(self) -> Optional[str]:
        return str(self._currency) if self._currency else None

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

    @property
    def value(self) -> str:
        return str(self)

    @property
    def sub_units(self) -> Decimal:
        if self._currency and isinstance(self._currency, BaseCurrencyType):
            if self._currency.decimal_digits == 0:
                output = self._amount
            else:
                output = self._amount * Decimal(pow(10, self._currency.decimal_digits))
        else:
            output = self._amount * 100

        if output == output.to_integral():
            return output.to_integral()
        return output

    def asdict(self) -> Dict[str, Optional[Union[str, int]]]:
        return {"value": self.value, "units": self.units, "nanos": self.nanos, "currency_code": self.currency_code}

    def as_dict(self) -> Dict[str, Optional[Union[str, int]]]:
        return self.asdict()

    def keys(self) -> List[str]:
        return list(self.asdict())

    def __getitem__(self, key: Any) -> Optional[Union[str, int]]:
        return self.asdict()[key]

    def as_string(self, *args: Any, **kwargs: Any) -> str:
        amount = self.amount_as_string(*args, **kwargs)

        if self._currency:
            return f"{amount} {self._currency}"
        return str(amount)

    def as_str(self, *args: Any, **kwargs: Any) -> str:
        return self.as_string(*args, **kwargs)

    def as_decimal(self) -> Decimal:
        return self._amount

    def as_int(self) -> int:
        return int(self)

    def as_float(self) -> float:
        return float(self)

    def as_json(self, keys: Union[List[str], Tuple[str, ...]] = ("value", "units", "nanos", "currency_code")) -> str:
        mapping = {
            "value": self.value,
            "units": self.units,
            "nanos": self.nanos,
            "amount": str(self.amount),
            "currency": self.currency_code,
            "currency_code": self.currency_code,
            "from_sub_units": False,
            "sub_units": self.sub_units,
        }

        output = {k: mapping.get(k) for k in keys if k in mapping}
        return json.dumps(output)

    def json(self, keys: Union[List[str], Tuple[str, ...]] = ("value", "units", "nanos", "currency_code")) -> str:
        return self.as_json(keys=keys)

    def as_protobuf(self, proto_class: Type[ProtobufMessageType] = MoneyProtobufMessage) -> ProtobufMessageType:  # type: ignore
        message: ProtobufMessageType = proto_class()

        mapping = {
            "value": self.value,
            "units": self.units,
            "nanos": self.nanos,
            "amount": str(self.amount),
            "currency": self.currency_code or "",
            "currency_code": self.currency_code or "",
            "from_sub_units": False,
        }

        for k, v in mapping.items():
            if hasattr(message, k):
                try:
                    setattr(message, k, type(getattr(message, k))(v))
                except TypeError:  # pragma: no cover
                    pass

        return message

    def as_proto(self, proto_class: Type[ProtobufMessageType] = MoneyProtobufMessage) -> ProtobufMessageType:  # type: ignore
        return self.as_protobuf(proto_class=proto_class)

    def protobuf(self, proto_class: Type[ProtobufMessageType] = MoneyProtobufMessage) -> ProtobufMessageType:  # type: ignore
        return self.as_protobuf(proto_class=proto_class)

    def proto(self, proto_class: Type[ProtobufMessageType] = MoneyProtobufMessage) -> ProtobufMessageType:  # type: ignore
        return self.as_protobuf(proto_class=proto_class)

    def is_signed(self) -> bool:
        return self._amount.is_signed()

    def is_zero(self) -> bool:
        return self._amount == 0

    def add(self, other: Any, from_sub_units: Optional[bool] = None) -> MoneyType:
        return self + self.__class__(other, from_sub_units=from_sub_units)

    def subtract(self, other: Any, from_sub_units: Optional[bool] = None) -> MoneyType:
        return self - self.__class__(other, from_sub_units=from_sub_units)

    def sub(self, other: Any, from_sub_units: Optional[bool] = None) -> MoneyType:
        return self.subtract(other, from_sub_units=from_sub_units)

    def to_integral(self) -> MoneyType:
        return self.__round__(0)

    def to_currency(self, currency: Optional[Union[CurrencyValue, str]]) -> MoneyType:
        return cast(MoneyType, self.__class__(self, currency=currency))

    def to(self, currency: Optional[Union[CurrencyValue, str]]) -> MoneyType:
        return self.to_currency(currency)

    def to_sub_units(self) -> MoneyType:
        if self._currency and isinstance(self._currency, BaseCurrencyType):
            if self._currency.decimal_digits == 0:
                return cast(MoneyType, self)
            return self * Decimal(pow(10, self._currency.decimal_digits))
        return self * 100

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of monetary amounts cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of monetary amounts cannot be deleted")

    def amount_as_string(self, min_decimals: Optional[int] = None, max_decimals: Optional[int] = None) -> str:
        if min_decimals is None and max_decimals is None:
            if self._currency and isinstance(self._currency, BaseCurrencyType):
                min_decimals = self._currency.decimal_digits
            min_decimals = DEFAULT_MIN_DECIMALS if min_decimals is None else min_decimals
            max_decimals = max(min_decimals, DEFAULT_MAX_DECIMALS)
        elif min_decimals is None and max_decimals is not None:
            if self._currency and isinstance(self._currency, BaseCurrencyType):
                min_decimals = self._currency.decimal_digits
            min_decimals = DEFAULT_MIN_DECIMALS if min_decimals is None else min_decimals
            min_decimals = min(min_decimals, max_decimals)
        elif min_decimals is not None and max_decimals is None:
            max_decimals = max(min_decimals, DEFAULT_MAX_DECIMALS)

        min_decimals = cast(int, min_decimals)
        max_decimals = cast(int, max_decimals)
        if min_decimals > max_decimals:
            raise ValueError("Invalid values for min_decimals and max_decimals")

        amount = self._amount.quantize(Decimal(f"1e-{min_decimals}"), ROUND_HALF_UP)
        if amount == 0:
            amount = Decimal(0).quantize(Decimal(f"1e-{min_decimals}"))
        if max_decimals > min_decimals and amount != self._amount.quantize(
            Decimal(f"1e-{max_decimals}"), ROUND_HALF_UP
        ):
            amount = self._amount.quantize(Decimal(f"1e-{max_decimals}"), ROUND_HALF_UP)
            value = f"{amount:f}".rstrip("0")
        else:
            value = f"{amount:f}"
        return value

    def __repr__(self) -> str:
        return f'<stockholm.Money: "{self}">'

    def __str__(self) -> str:
        return self.as_string()

    def __format__(self, format_spec: str) -> str:
        if not format_spec:
            return str(self)

        m = _parse_format_specifier_regex.match(format_spec)
        if m is None:
            raise ValueError(f"Invalid format specifier: {format_spec}")

        format_dict = m.groupdict()

        fill = format_dict["fill"]
        align = format_dict["align"]
        zeropad = format_dict["zeropad"] is not None
        if zeropad:
            if fill is not None:
                raise ValueError(f"Fill character conflicts with '0' in format specifier: {format_spec}")
            if align is not None:
                raise ValueError(f"Alignment conflicts with '0' in format specifier: {format_spec}")
            fill = "0"
            align = ">"
        fill = fill or " "
        align = align or ">"

        sign = format_dict["sign"] or "-"

        minimumwidth = int(format_dict["minimumwidth"] or 0)
        precision = int(format_dict["precision"]) if format_dict["precision"] is not None else None

        thousands_sep = format_dict["thousands_sep"] if format_dict["thousands_sep"] is not None else ""

        output = ""

        if format_dict["type"] == "c":
            output = str(self._currency or "")

        if format_dict["type"] == "d":
            format_dict["type"] = "f"
            precision = 0

        with decimal.localcontext(RoundingContext):
            if format_dict["type"] in ("m", "M", "f", "F"):
                if precision is not None:
                    output = self.amount_as_string(min_decimals=precision, max_decimals=precision)
                else:
                    output = self.amount_as_string()

                output_amount = Money(output).amount

                if thousands_sep and (output_amount >= 1000 or output_amount <= -1000):
                    integral = int(output.split(".")[0])
                    try:
                        decimals = output.split(".")[1]
                        output = f"{integral:{thousands_sep}.0f}.{decimals}"
                    except IndexError:
                        output = f"{integral:{thousands_sep}.0f}"

                if format_dict["align"] == "=":
                    format_dict["align"] = ""
                    zeropad = True

                if zeropad:
                    if output.startswith("-"):
                        output = output[1:].rjust(minimumwidth - 1, fill)
                        output = f"-{output}"
                    else:
                        output = output.rjust(minimumwidth, fill)
                    if sign != "-" and output_amount >= 0:
                        if output.startswith(fill) and not output.startswith("0."):
                            output = f"{sign}{output[1:]}"
                        else:
                            output = f"{sign}{output}"
                elif sign != "-" and output_amount >= 0:
                    output = f"{sign}{output}"

                if not zeropad and not format_dict["align"] and align and fill and minimumwidth:
                    output = f"{output:{fill}{align}{minimumwidth}}"

                zeropad = False
                sign = ""
                thousands_sep = ""

                if self._currency:
                    if format_dict["type"] == "m":
                        output = f"{output} {self._currency}"
                    elif format_dict["type"] == "M":
                        output = f"{self._currency} {output}"
            elif format_dict["type"] in ("s", "", None):
                format_dict["type"] = "s"
                output = self.as_string()

        if sign and format_dict["sign"]:
            raise ValueError("Sign not allowed in string format specifier")
        if zeropad or format_dict["align"] == "=":
            raise ValueError("'=' alignment not allowed in string format specifier")
        if thousands_sep:
            raise ValueError("Cannot specify ',' in string format specifier")

        if format_dict["align"] and align and fill and minimumwidth:
            output = f"{output:{fill}{align}{minimumwidth}}"

        return output

    def __hash__(self) -> int:
        return hash(("stockholm.Money", self._amount, self._currency))

    def __bool__(self) -> bool:
        return bool(self._amount)

    def _convert_other(self, other: Any, allow_currency_mismatch: bool = False) -> MoneyType:
        if not isinstance(other, Money):
            try:
                converted_other: MoneyType = cast(MoneyType, self.__class__(other))
            except ConversionError as ex:
                other_repr = repr(other)
                self_repr = repr(self)
                raise InvalidOperandError(f"Unable to perform operations on {self_repr} with {other_repr}") from ex
        else:
            converted_other = cast(MoneyType, other)

        if (
            not allow_currency_mismatch
            and self._currency
            and converted_other._currency
            and self._currency != converted_other._currency
        ):
            raise CurrencyMismatchError("Unable to perform operations on values with differing currencies")

        return converted_other

    def _preferred_currency(self, other: MoneyType) -> Optional[Union[CurrencyValue, str]]:
        currency = self._currency if self._currency and isinstance(self._currency, BaseCurrencyType) else None
        currency = other._currency if not currency and other._currency and isinstance(other, BaseCurrencyType) else None
        return currency or self._currency or other._currency

    def __eq__(self, other: Any) -> bool:
        try:
            converted_other = self._convert_other(other, allow_currency_mismatch=True)
        except (ConversionError, InvalidOperandError):
            return False

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

    def __add__(self, other: Any) -> MoneyType:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        converted_other = self._convert_other(other)
        amount = self._amount + converted_other._amount
        currency = self._preferred_currency(converted_other)

        return cls(amount, currency=currency)

    def __radd__(self, other: Any) -> MoneyType:
        return self.__add__(other)

    def __sub__(self, other: Any) -> MoneyType:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        converted_other = self._convert_other(other)
        amount = self._amount - converted_other._amount
        currency = self._preferred_currency(converted_other)

        return cls(amount, currency=currency)

    def __rsub__(self, other: Any) -> MoneyType:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        converted_other = self._convert_other(other)
        amount = converted_other._amount - self._amount
        currency = self._preferred_currency(converted_other)

        return cls(amount, currency=currency)

    def __mul__(self, other: Any) -> MoneyType:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        if not isinstance(other, Money):
            converted_other = self._convert_other(other)
        else:
            converted_other = cast(MoneyType, other)

        if converted_other._currency is not None and self._currency is not None:
            raise InvalidOperandError("Unable to multiply two monetary amounts with each other")

        amount = self._amount * converted_other._amount
        currency = self._preferred_currency(converted_other)
        return cls(amount, currency=currency)

    def __rmul__(self, other: Any) -> MoneyType:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> MoneyType:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        converted_other = self._convert_other(other, allow_currency_mismatch=True)

        if converted_other.amount == 0:
            raise ZeroDivisionError("division by zero")

        amount = self._amount / converted_other._amount

        if converted_other._currency is not None:
            return cls(amount, currency=None)

        return cls(amount, currency=self._currency)

    def __floordiv__(self, other: Any) -> MoneyType:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        converted_other = self._convert_other(other, allow_currency_mismatch=True)

        if converted_other.amount == 0:
            raise ZeroDivisionError("division by zero")

        amount = self._amount // converted_other._amount

        if converted_other._currency is not None:
            return cls(amount, currency=None)

        return cls(amount, currency=self._currency)

    def __mod__(self, other: Any) -> MoneyType:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        converted_other = self._convert_other(other, allow_currency_mismatch=True)
        amount = self._amount % converted_other._amount

        if self._currency == converted_other._currency:
            currency = self._preferred_currency(converted_other)
        else:
            currency = self._currency

        return cls(amount, currency=currency)

    def __divmod__(self, other: Any) -> Tuple[MoneyType, MoneyType]:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        converted_other = self._convert_other(other, allow_currency_mismatch=True)
        quotient, remainder = divmod(self._amount, converted_other._amount)

        if self._currency == converted_other._currency:
            currency = self._preferred_currency(converted_other)
        else:
            currency = self._currency

        if converted_other._currency is not None:
            return cls(quotient), cls(remainder, currency=currency)

        return cls(quotient, currency=currency), cls(remainder, currency=currency)

    def __pow__(self, other: Any) -> MoneyType:
        cls: Type[MoneyType] = self.__class__ if self.__class__ == other.__class__ else Money

        if not isinstance(other, Money):
            converted_other = self._convert_other(other)
        else:
            converted_other = cast(MoneyType, other)

        if converted_other._currency is not None:
            raise InvalidOperandError("Unable to use a monetary amount as an exponent")

        amount = self._amount**converted_other._amount
        return cls(amount, currency=self._currency)

    def __neg__(self) -> MoneyType:
        return cast(MoneyType, self.__class__(-self._amount, currency=self._currency))

    def __pos__(self) -> MoneyType:
        return cast(MoneyType, self.__class__(+self._amount, currency=self._currency))

    def __abs__(self) -> MoneyType:
        return cast(MoneyType, self.__class__(abs(self._amount), currency=self._currency))

    def __int__(self) -> int:
        return int(self._amount)

    def __float__(self) -> float:
        return float(self._amount)

    def __round__(self, ndigits: int = 0) -> MoneyType:
        with decimal.localcontext(RoundingContext):
            amount = round(self._amount, ndigits)

        return cast(MoneyType, self.__class__(amount, currency=self._currency))


class Money(MoneyModel):
    @classmethod
    def from_sub_units(
        cls,
        amount: Optional[Union[MoneyType, Decimal, int, float, str, object]],
        currency: Optional[Union[DefaultCurrencyValue, CurrencyValue, str]] = DefaultCurrency,
        value: Optional[Union[MoneyType, Decimal, int, float, str]] = None,
        currency_code: Optional[str] = None,
        **kwargs: Any,
    ) -> "Money":
        return cast(
            Money,
            super().from_sub_units(
                amount=amount, currency=currency, value=value, currency_code=currency_code, **kwargs
            ),
        )

    @classmethod
    def from_dict(cls, input_dict: Dict) -> "Money":
        return cls(**input_dict)

    @classmethod
    def from_json(cls, input_value: Union[str, bytes]) -> "Money":
        return cls(**json.loads(input_value))

    @classmethod
    def from_protobuf(
        cls, input_value: Union[str, bytes, object], proto_class: Type[GenericProtobufMessage] = MoneyProtobufMessage
    ) -> "Money":
        if input_value is not None and isinstance(input_value, bytes):
            input_value = proto_class.FromString(input_value)

        return cls(
            **{
                k: getattr(input_value, k)
                for k in (
                    "value",
                    "units",
                    "nanos",
                    "amount",
                    "currency",
                    "currency_code",
                    "from_sub_units",
                )
                if hasattr(input_value, k)
            }
        )

    @classmethod
    def from_proto(
        cls, input_value: Union[str, bytes, object], proto_class: Type[GenericProtobufMessage] = MoneyProtobufMessage
    ) -> "Money":
        return cls.from_protobuf(input_value, proto_class=proto_class)
