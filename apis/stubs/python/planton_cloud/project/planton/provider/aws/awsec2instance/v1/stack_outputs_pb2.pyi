from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEc2InstanceStackOutputs(_message.Message):
    __slots__ = ("instance_id", "private_ip", "private_dns_name", "availability_zone", "instance_profile_arn", "ssh_private_key", "ssh_public_key")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_IP_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_ZONE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_PROFILE_ARN_FIELD_NUMBER: _ClassVar[int]
    SSH_PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    SSH_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    private_ip: str
    private_dns_name: str
    availability_zone: str
    instance_profile_arn: str
    ssh_private_key: str
    ssh_public_key: str
    def __init__(self, instance_id: _Optional[str] = ..., private_ip: _Optional[str] = ..., private_dns_name: _Optional[str] = ..., availability_zone: _Optional[str] = ..., instance_profile_arn: _Optional[str] = ..., ssh_private_key: _Optional[str] = ..., ssh_public_key: _Optional[str] = ...) -> None: ...
