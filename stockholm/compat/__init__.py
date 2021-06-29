import sys

try:
    from typing import Protocol  # noqa
except ImportError:  # pragma: no cover
    # Compatibility import for Python 3.7
    this_module = sys.modules[__name__]
    from typing_extensions import Protocol as _Protocol  # noqa

    setattr(this_module, "Protocol", _Protocol)  # noqa
