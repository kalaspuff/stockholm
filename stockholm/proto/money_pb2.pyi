# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from typing import Optional as typing___Optional
from typing import Text as typing___Text

from google.protobuf.descriptor import Descriptor as google___protobuf___descriptor___Descriptor
from google.protobuf.descriptor import FileDescriptor as google___protobuf___descriptor___FileDescriptor
from google.protobuf.message import Message as google___protobuf___message___Message
from typing_extensions import Literal as typing_extensions___Literal

builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int

DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class Money(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    currency_code: typing___Text = ...
    units: builtin___int = ...
    nanos: builtin___int = ...
    def __init__(
        self,
        *,
        currency_code: typing___Optional[typing___Text] = None,
        units: typing___Optional[builtin___int] = None,
        nanos: typing___Optional[builtin___int] = None,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "currency_code", b"currency_code", "nanos", b"nanos", "units", b"units"
        ],
    ) -> None: ...

type___Money = Money
