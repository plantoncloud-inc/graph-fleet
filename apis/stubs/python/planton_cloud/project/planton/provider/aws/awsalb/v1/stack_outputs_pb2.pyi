from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsAlbStackOutputs(_message.Message):
    __slots__ = ("load_balancer_arn", "load_balancer_name", "load_balancer_dns_name", "load_balancer_hosted_zone_id")
    LOAD_BALANCER_ARN_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_NAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_HOSTED_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    load_balancer_arn: str
    load_balancer_name: str
    load_balancer_dns_name: str
    load_balancer_hosted_zone_id: str
    def __init__(self, load_balancer_arn: _Optional[str] = ..., load_balancer_name: _Optional[str] = ..., load_balancer_dns_name: _Optional[str] = ..., load_balancer_hosted_zone_id: _Optional[str] = ...) -> None: ...
