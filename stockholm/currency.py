from typing import Any, Optional, Union

class Currency:
    __slots__ = ("_ticker", "_currency")
    _ticker: Optional[str]

    @property
    def ticker(self) -> Optional[str]:
        return self._ticker or ""

    def __init__(self, currency: Optional[Union["Currency", str]]) -> None:
        if currency and isinstance(currency, str):
            object.__setattr__(self, "_ticker", currency)
        if currency and isinstance(currency, Currency):
            object.__setattr__(self, "_ticker", currency._ticker)
        print(self)

    def __setattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of monetary amounts cannot be changed")

    def __delattr__(self, *args: Any) -> None:
        raise AttributeError("Attributes of monetary amounts cannot be deleted")

    def __repr__(self) -> str:
        return f'<stockholm.Currency: "{self}">'

    def __str__(self) -> str:
        return self._ticker or ""

    def __format__(self, format_spec: str) -> str:
        output = str(self)
        return f"{output:{format_spec}}"

    def __eq__(self, other: Optional[Union["Currency", str]]) -> bool:
        if self._ticker:
            if not other:
                return False
            if isinstance(other, Currency):
                return self._ticker == other._ticker
            if isinstance(other, str):
                return self._ticker == other
        if isinstance(other, Currency):
            return not other._ticker
        return not other
