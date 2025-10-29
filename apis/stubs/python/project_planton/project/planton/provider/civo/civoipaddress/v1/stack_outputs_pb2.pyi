from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoIpAddressStackOutputs(_message.Message):
    __slots__ = ("reserved_ip_id", "ip_address", "attached_resource_id", "created_at_rfc3339")
    RESERVED_IP_ID_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ATTACHED_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_RFC3339_FIELD_NUMBER: _ClassVar[int]
    reserved_ip_id: str
    ip_address: str
    attached_resource_id: str
    created_at_rfc3339: str
    def __init__(self, reserved_ip_id: _Optional[str] = ..., ip_address: _Optional[str] = ..., attached_resource_id: _Optional[str] = ..., created_at_rfc3339: _Optional[str] = ...) -> None: ...
