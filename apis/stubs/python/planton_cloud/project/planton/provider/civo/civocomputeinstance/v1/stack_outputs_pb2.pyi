from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoComputeInstanceStackOutputs(_message.Message):
    __slots__ = ("instance_id", "public_ipv4", "private_ipv4", "status", "created_at_rfc3339")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IPV4_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_IPV4_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_RFC3339_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    public_ipv4: str
    private_ipv4: str
    status: str
    created_at_rfc3339: str
    def __init__(self, instance_id: _Optional[str] = ..., public_ipv4: _Optional[str] = ..., private_ipv4: _Optional[str] = ..., status: _Optional[str] = ..., created_at_rfc3339: _Optional[str] = ...) -> None: ...
