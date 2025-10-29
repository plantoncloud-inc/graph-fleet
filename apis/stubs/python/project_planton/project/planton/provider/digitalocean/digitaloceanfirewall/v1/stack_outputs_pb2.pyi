from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanFirewallStackOutputs(_message.Message):
    __slots__ = ("firewall_id",)
    FIREWALL_ID_FIELD_NUMBER: _ClassVar[int]
    firewall_id: str
    def __init__(self, firewall_id: _Optional[str] = ...) -> None: ...
