from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareD1DatabaseStackOutputs(_message.Message):
    __slots__ = ("database_id", "database_name", "connection_string")
    DATABASE_ID_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_STRING_FIELD_NUMBER: _ClassVar[int]
    database_id: str
    database_name: str
    connection_string: str
    def __init__(self, database_id: _Optional[str] = ..., database_name: _Optional[str] = ..., connection_string: _Optional[str] = ...) -> None: ...
