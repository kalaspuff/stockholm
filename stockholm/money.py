import re

from decimal import Decimal, ROUND_HALF_UP


__all__ = ["Money"]


class Money:
    __slots__ = ("_amount", "_currency", "_metadata")

    def __init__(self, amount=None, currency=None, is_cents=False, **kwargs):
        if currency is not None and not isinstance(currency, str):
            raise Exception("Invalid currency")

        output_amount = None
        output_currency = currency.strip().upper() if currency and currency.strip() else None

        if amount is not None and isinstance(amount, int) and not isinstance(amount, bool):
            if is_cents:
                output_amount = Decimal(amount) / 100
            else:
                output_amount = Decimal(amount)
        if amount is not None and isinstance(amount, float):
            if is_cents:
                output_amount = Decimal(str(amount)) / 100
            else:
                output_amount = Decimal(str(amount))
        elif amount is not None and isinstance(amount, str) and amount.strip():
            amount = amount.strip()
            matches = re.match(r'^([-+]?[0-9.]+)[ ]+([a-zA-Z._-]+)$', amount)
            match_currency = None
            if matches:
                amount = matches.group(1).strip()
                match_currency = matches.group(2).strip().upper()
            else:
                matches = re.match(r'^([a-zA-Z._-]+)[ ]+([-+]?[0-9.]+)$', amount)
                if matches:
                    amount = matches.group(2).strip()
                    match_currency = matches.group(1).strip().upper()

            if match_currency is not None:
                if output_currency is not None and match_currency != output_currency:
                    raise Exception("Mismatching currency in input amount string and currency argument")
                output_currency = match_currency

            try:
                if is_cents:
                    output_amount = Decimal(amount) / 100
                else:
                    output_amount = Decimal(amount)
            except Exception:
                raise Exception("Value cannot be used as monetary amount")

        if output_amount is None:
            raise Exception("Missing input values for valid monetary amount")

        if output_amount == 0 and str(output_amount).startswith("-"):
            output_amount = Decimal(str(output_amount)[1:])

        object.__setattr__(self, "_amount", output_amount)
        object.__setattr__(self, "_currency", output_currency)

        output_metadata = {
            "is_cents": bool(is_cents)
        }
        object.__setattr__(self, "_metadata", output_metadata)

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    def __setattr__(self, *args):
        raise AttributeError("Attributes of stockholm.Money cannot be changed")

    def __delattr__(self, *args):
        raise AttributeError("Attributes of stockholm.Money cannot be deleted")

    def _str_amount(self, min_decimals=2, max_decimals=9):
        try:
            decimals = len(str(self._amount).split('.')[1][0:max_decimals].rstrip("0"))
        except Exception:
            decimals = min_decimals

        decimals = min(max(min_decimals, decimals), max_decimals)

        return str(self._amount.quantize(Decimal(f"1e-{decimals}"), ROUND_HALF_UP))

    def __repr__(self):
        amount = self._str_amount()
        if self._currency:
            return f"<stockholm.Money: \"{amount} {self._currency}\">"
        return f"<stockholm.Money: \"{amount}\">"

    def __str__(self):
        amount = self._str_amount()

        if self._currency:
            return f"{amount} {self._currency}"
        return str(amount)

    def __hash__(self):
        return hash(("stockholm", self._amount, self._currency, frozenset(self._metadata)))

    def __bool__(self):
        return bool(self._amount)

    def _convert_other(self, other):
        if not isinstance(other, Money):
            try:
                other = Money(other)
            except Exception:
                other_repr = repr(other)
                self_repr = repr(self)
                raise Exception(f"Unable to compare {self_repr} with {other_repr}")

        if self._currency and other.currency and self._currency != other.currency:
            raise Exception("Unable to compare difference in values with differing currencies")

        return other

    def __eq__(self, other):
        if not isinstance(other, Money):
            try:
                other = Money(other)
            except Exception:
                return False

        if self._currency and other.currency and self._currency != other.currency:
            if self.amount == 0 and other.amount == 0:
                return True
            return False
        return self._amount == other.amount

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        other = self._convert_other(other)
        return self.amount < other.amount

    def __le__(self, other):
        other = self._convert_other(other)
        return self.amount <= other.amount

    def __gt__(self, other):
        other = self._convert_other(other)
        return self.amount > other.amount

    def __ge__(self, other):
        other = self._convert_other(other)
        return self.amount >= other.amount
