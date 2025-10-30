from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GoogleServiceAccount(_message.Message):
    __slots__ = ("email", "key_base64")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    email: str
    key_base64: str
    def __init__(self, email: _Optional[str] = ..., key_base64: _Optional[str] = ...) -> None: ...
