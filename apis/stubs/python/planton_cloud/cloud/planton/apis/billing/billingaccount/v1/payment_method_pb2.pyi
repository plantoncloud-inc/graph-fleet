from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IsDefaultPaymentMethodExists(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: bool = ...) -> None: ...

class InitiateCheckoutSessionInput(_message.Message):
    __slots__ = ("org", "set_as_default")
    ORG_FIELD_NUMBER: _ClassVar[int]
    SET_AS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    org: str
    set_as_default: bool
    def __init__(self, org: _Optional[str] = ..., set_as_default: bool = ...) -> None: ...

class CheckoutUrl(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class CheckoutSessionId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...
