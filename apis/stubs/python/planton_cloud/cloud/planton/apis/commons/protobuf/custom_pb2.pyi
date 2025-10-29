from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CustomEmpty(_message.Message):
    __slots__ = ("is_empty",)
    IS_EMPTY_FIELD_NUMBER: _ClassVar[int]
    is_empty: bool
    def __init__(self, is_empty: bool = ...) -> None: ...
