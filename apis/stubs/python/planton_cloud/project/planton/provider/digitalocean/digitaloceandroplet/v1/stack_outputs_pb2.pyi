from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanDropletStackOutputs(_message.Message):
    __slots__ = ("droplet_id", "ipv4_address", "ipv6_address", "image_id", "vpc_uuid")
    DROPLET_ID_FIELD_NUMBER: _ClassVar[int]
    IPV4_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IPV6_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    VPC_UUID_FIELD_NUMBER: _ClassVar[int]
    droplet_id: str
    ipv4_address: str
    ipv6_address: str
    image_id: int
    vpc_uuid: str
    def __init__(self, droplet_id: _Optional[str] = ..., ipv4_address: _Optional[str] = ..., ipv6_address: _Optional[str] = ..., image_id: _Optional[int] = ..., vpc_uuid: _Optional[str] = ...) -> None: ...
