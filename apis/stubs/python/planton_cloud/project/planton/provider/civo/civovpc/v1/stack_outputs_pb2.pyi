from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoVpcStackOutputs(_message.Message):
    __slots__ = ("network_id", "cidr_block", "created_at_rfc3339")
    NETWORK_ID_FIELD_NUMBER: _ClassVar[int]
    CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_RFC3339_FIELD_NUMBER: _ClassVar[int]
    network_id: str
    cidr_block: str
    created_at_rfc3339: str
    def __init__(self, network_id: _Optional[str] = ..., cidr_block: _Optional[str] = ..., created_at_rfc3339: _Optional[str] = ...) -> None: ...
