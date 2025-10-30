from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareKvNamespaceSpec(_message.Message):
    __slots__ = ("namespace_name", "ttl_seconds", "description")
    NAMESPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    namespace_name: str
    ttl_seconds: int
    description: str
    def __init__(self, namespace_name: _Optional[str] = ..., ttl_seconds: _Optional[int] = ..., description: _Optional[str] = ...) -> None: ...
