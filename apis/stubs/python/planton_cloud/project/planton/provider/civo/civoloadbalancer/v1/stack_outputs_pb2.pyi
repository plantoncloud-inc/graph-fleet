from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoLoadBalancerStackOutputs(_message.Message):
    __slots__ = ("load_balancer_id", "ip_address", "dns_name", "created_at_rfc3339")
    LOAD_BALANCER_ID_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_RFC3339_FIELD_NUMBER: _ClassVar[int]
    load_balancer_id: str
    ip_address: str
    dns_name: str
    created_at_rfc3339: str
    def __init__(self, load_balancer_id: _Optional[str] = ..., ip_address: _Optional[str] = ..., dns_name: _Optional[str] = ..., created_at_rfc3339: _Optional[str] = ...) -> None: ...
