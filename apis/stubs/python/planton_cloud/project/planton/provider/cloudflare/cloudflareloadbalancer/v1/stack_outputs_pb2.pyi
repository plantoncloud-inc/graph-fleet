from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareLoadBalancerStackOutputs(_message.Message):
    __slots__ = ("load_balancer_id", "load_balancer_dns_record_name", "load_balancer_cname_target")
    LOAD_BALANCER_ID_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_DNS_RECORD_NAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_CNAME_TARGET_FIELD_NUMBER: _ClassVar[int]
    load_balancer_id: str
    load_balancer_dns_record_name: str
    load_balancer_cname_target: str
    def __init__(self, load_balancer_id: _Optional[str] = ..., load_balancer_dns_record_name: _Optional[str] = ..., load_balancer_cname_target: _Optional[str] = ...) -> None: ...
