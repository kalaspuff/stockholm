"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class Money(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CURRENCY_CODE_FIELD_NUMBER: builtins.int
    UNITS_FIELD_NUMBER: builtins.int
    NANOS_FIELD_NUMBER: builtins.int
    currency_code: typing.Text = ...
    units: builtins.int = ...
    nanos: builtins.int = ...
    def __init__(
        self,
        *,
        currency_code: typing.Text = ...,
        units: builtins.int = ...,
        nanos: builtins.int = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal["currency_code", b"currency_code", "nanos", b"nanos", "units", b"units"],
    ) -> None: ...

global___Money = Money
