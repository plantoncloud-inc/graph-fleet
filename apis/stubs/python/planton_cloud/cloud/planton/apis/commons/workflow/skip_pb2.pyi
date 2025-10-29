from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SkipDecision(_message.Message):
    __slots__ = ("skip", "reason")
    SKIP_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    skip: bool
    reason: str
    def __init__(self, skip: bool = ..., reason: _Optional[str] = ...) -> None: ...
