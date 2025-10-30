from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanLoadBalancerStackOutputs(_message.Message):
    __slots__ = ("load_balancer_id", "ip", "dns_name")
    LOAD_BALANCER_ID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    load_balancer_id: str
    ip: str
    dns_name: str
    def __init__(self, load_balancer_id: _Optional[str] = ..., ip: _Optional[str] = ..., dns_name: _Optional[str] = ...) -> None: ...
