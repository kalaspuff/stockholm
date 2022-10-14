import sys
from typing import Any

try:
    from google.protobuf.message import Message as GenericProtobufMessage  # noqa
except Exception:  # pragma: no cover

    class _GenericProtobufMessage(object):
        pass

    this_module = sys.modules[__name__]
    setattr(this_module, "GenericProtobufMessage", _GenericProtobufMessage)

try:
    from .money_pb2 import Money  # noqa

    MoneyProtobufMessage = Money
except Exception:  # pragma: no cover

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
