from typing import Any, Dict, Optional, Tuple, Type, TypeVar, Union


class MetaCurrency(type):
    def __new__(cls, name: str, bases: Tuple[type, ...], attributedict: Dict) -> type:
        ticker = attributedict.get('ticker', attributedict.get('_ticker', attributedict.get('__qualname__')))
        attributedict["ticker"] = ticker.split(".")[-1] if ticker else ""
        attributedict["currency"] = attributedict["ticker"]

        result: Type[Currency] = type.__new__(cls, name, bases, attributedict)
        return result

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be deleted")

    def __repr__(self) -> str:
        return f'<stockholm.Currency: "{self}">'

    def __str__(self) -> str:
        return self.ticker or ""

    def __format__(self, format_spec: str) -> str:
        output = str(self)
        return f"{output:{format_spec}}"

    def __eq__(self, other: Any) -> bool:
        if self.ticker:
            if not other:
                return False
            if isinstance(other, Currency):
                return self.ticker == other.ticker
            if isinstance(other, str):
                return self.ticker == other
        else:
            if isinstance(other, Currency):
                return not other.ticker
            if isinstance(other, str):
                return other == ""
            return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    @property
    def __class__(self):
        return Currency

    def __hash__(self) -> int:
        return hash(("stockholm.MetaCurrency", self.ticker))

    def __bool__(self) -> bool:
        return bool(self.ticker)


class Currency(metaclass=MetaCurrency):
    def __init__(self, currency: Optional[Union["Currency", str]] = None) -> None:
        if currency and isinstance(currency, str):
            object.__setattr__(self, "ticker", currency)
        elif currency and isinstance(currency, Currency):
            object.__setattr__(self, "ticker", currency.ticker)
        else:
            object.__setattr__(self, "ticker", "")

        object.__setattr__(self, "currency", self.ticker)

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of currencies cannot be deleted")

    def __repr__(self) -> str:
        return f'<stockholm.Currency: "{self.ticker}">'

    def __str__(self) -> str:
        return self.ticker or ""

    def __format__(self, format_spec: str) -> str:
        output = str(self)
        return f"{output:{format_spec}}"

    def __eq__(self, other: Any) -> bool:
        if self.ticker:
            if not other:
                return False
            if isinstance(other, Currency):
                return self.ticker == other.ticker
            if isinstance(other, str):
                return self.ticker == other
        else:
            if isinstance(other, Currency):
                return not other.ticker
            if isinstance(other, str):
                return other == ""
            return False

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(("stockholm.Currency", self.ticker))

    def __bool__(self) -> bool:
        return bool(self.ticker)
