from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MongodbAtlasCredentialSpec(_message.Message):
    __slots__ = ("public_key", "private_key")
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    public_key: str
    private_key: str
    def __init__(self, public_key: _Optional[str] = ..., private_key: _Optional[str] = ...) -> None: ...
