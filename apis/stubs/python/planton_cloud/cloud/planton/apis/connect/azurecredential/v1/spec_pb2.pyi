from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AzureCredentialSpec(_message.Message):
    __slots__ = ("client_id", "client_secret", "tenant_id", "subscription_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    tenant_id: str
    subscription_id: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., tenant_id: _Optional[str] = ..., subscription_id: _Optional[str] = ...) -> None: ...
