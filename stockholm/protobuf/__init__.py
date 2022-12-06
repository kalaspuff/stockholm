import sys
from typing import Any

try:
    from google.protobuf.message import Message as GenericProtobufMessage  # noqa isort:skip
except Exception:  # pragma: no cover

    class _GenericProtobufMessage(object):
        pass

    this_module = sys.modules[__name__]
    setattr(this_module, "GenericProtobufMessage", _GenericProtobufMessage)

try:
    from google.type.money_pb2 import Money, Money as MoneyProtobufMessage  # noqa isort:skip
except Exception:  # pragma: no cover
    try:
        from google.type import Money, Money as MoneyProtobufMessage  # noqa isort:skip
    except Exception:
        try:
            from .money_pb2 import Money, Money as MoneyProtobufMessage  # noqa isort:skip
        except Exception:

            class _MoneyProtobufMessage(object):
                def __init__(self, *args: Any, **kwargs: Any) -> None:
                    raise Exception("google.protobuf package not installed")

                def SerializeToString(self, *args: Any, **kwargs: Any) -> None:
                    raise Exception("google.protobuf package not installed")

                def FromString(self, *args: Any, **kwargs: Any) -> None:
                    raise Exception("google.protobuf package not installed")

                def ParseFromString(self, *args: Any, **kwargs: Any) -> None:
                    raise Exception("google.protobuf package not installed")

                def MergeFromString(self, *args: Any, **kwargs: Any) -> None:
                    raise Exception("google.protobuf package not installed")

            this_module = sys.modules[__name__]
            setattr(this_module, "Money", _MoneyProtobufMessage)
            setattr(this_module, "MoneyProtobufMessage", _MoneyProtobufMessage)


__all__ = [
    "GenericProtobufMessage",
    "Money",
    "MoneyProtobufMessage",
]
