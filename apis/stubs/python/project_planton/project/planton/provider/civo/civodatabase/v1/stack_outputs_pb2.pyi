from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoDatabaseStackOutputs(_message.Message):
    __slots__ = ("database_id", "host", "port", "username", "password_secret_ref", "replica_endpoints")
    DATABASE_ID_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_SECRET_REF_FIELD_NUMBER: _ClassVar[int]
    REPLICA_ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    database_id: str
    host: str
    port: int
    username: str
    password_secret_ref: str
    replica_endpoints: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, database_id: _Optional[str] = ..., host: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ..., password_secret_ref: _Optional[str] = ..., replica_endpoints: _Optional[_Iterable[str]] = ...) -> None: ...
