from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanVpcSpec(_message.Message):
    __slots__ = ("description", "region", "ip_range_cidr", "is_default_for_region")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    IP_RANGE_CIDR_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FOR_REGION_FIELD_NUMBER: _ClassVar[int]
    description: str
    region: _region_pb2.DigitalOceanRegion
    ip_range_cidr: str
    is_default_for_region: bool
    def __init__(self, description: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., ip_range_cidr: _Optional[str] = ..., is_default_for_region: bool = ...) -> None: ...
