from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConfluentProviderConfig(_message.Message):
    __slots__ = ("api_key", "api_secret")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    API_SECRET_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    api_secret: str
    def __init__(self, api_key: _Optional[str] = ..., api_secret: _Optional[str] = ...) -> None: ...
