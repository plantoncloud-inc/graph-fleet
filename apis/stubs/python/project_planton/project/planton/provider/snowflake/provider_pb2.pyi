from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SnowflakeProviderConfig(_message.Message):
    __slots__ = ("account", "region", "username", "password")
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    account: str
    region: str
    username: str
    password: str
    def __init__(self, account: _Optional[str] = ..., region: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...
