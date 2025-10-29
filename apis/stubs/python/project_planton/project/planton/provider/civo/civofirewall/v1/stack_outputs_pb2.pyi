from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoFirewallStackOutputs(_message.Message):
    __slots__ = ("firewall_id", "created_at_rfc3339")
    FIREWALL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_RFC3339_FIELD_NUMBER: _ClassVar[int]
    firewall_id: str
    created_at_rfc3339: str
    def __init__(self, firewall_id: _Optional[str] = ..., created_at_rfc3339: _Optional[str] = ...) -> None: ...
