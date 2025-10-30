from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanDatabaseClusterStackOutputs(_message.Message):
    __slots__ = ("cluster_id", "connection_uri", "host", "port", "database_user", "database_password")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_URI_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    DATABASE_USER_FIELD_NUMBER: _ClassVar[int]
    DATABASE_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    connection_uri: str
    host: str
    port: int
    database_user: str
    database_password: str
    def __init__(self, cluster_id: _Optional[str] = ..., connection_uri: _Optional[str] = ..., host: _Optional[str] = ..., port: _Optional[int] = ..., database_user: _Optional[str] = ..., database_password: _Optional[str] = ...) -> None: ...
