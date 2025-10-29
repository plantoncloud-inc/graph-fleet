from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TestCloudResourceThreeSpec(_message.Message):
    __slots__ = ("placeholder",)
    PLACEHOLDER_FIELD_NUMBER: _ClassVar[int]
    placeholder: str
    def __init__(self, placeholder: _Optional[str] = ...) -> None: ...
