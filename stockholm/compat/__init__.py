import sys
from typing import List, Optional, Set, Tuple, Type, Union

try:
    from typing import Protocol

    class CurrencyValue(Protocol):
        ticker: str
        decimal_digits: int
        interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]]
        preferred_ticker: Optional[str]

except ImportError:  # pragma: no cover
    # Compatibility import for Python 3.7
    this_module = sys.modules[__name__]
    try:
        from typing_extensions import Protocol as _Protocol  # noqa

        class _CurrencyValue(_Protocol):
            ticker: str
            decimal_digits: int
            interchangeable_with: Optional[Union[Tuple[str, ...], List[str], Set[str]]]
            preferred_ticker: Optional[str]

        setattr(this_module, "Protocol", _Protocol)  # noqa
        setattr(this_module, "CurrencyValue", _CurrencyValue)  # noqa
    except ModuleNotFoundError:  # pragma: no cover

        class _ProtocolProxy:
            pass

        from stockholm.currency import BaseCurrency, BaseCurrencyType, MetaCurrency

        _CurrencyValueProxy = Union[BaseCurrency, BaseCurrencyType, MetaCurrency, Type[BaseCurrencyType]]

        setattr(this_module, "Protocol", _ProtocolProxy)  # noqa
        setattr(this_module, "CurrencyValue", _CurrencyValueProxy)  # noqa


__all__ = [
    "Protocol",
    "CurrencyValue",
]
