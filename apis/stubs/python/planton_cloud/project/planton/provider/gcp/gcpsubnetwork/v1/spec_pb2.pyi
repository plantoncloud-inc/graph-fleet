from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpSubnetworkSpec(_message.Message):
    __slots__ = ("project_id", "vpc_self_link", "region", "ip_cidr_range", "secondary_ip_ranges", "private_ip_google_access")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    VPC_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    IP_CIDR_RANGE_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_IP_RANGES_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_IP_GOOGLE_ACCESS_FIELD_NUMBER: _ClassVar[int]
    project_id: _foreign_key_pb2.StringValueOrRef
    vpc_self_link: _foreign_key_pb2.StringValueOrRef
    region: str
    ip_cidr_range: str
    secondary_ip_ranges: _containers.RepeatedCompositeFieldContainer[GcpSubnetworkSecondaryRange]
    private_ip_google_access: bool
    def __init__(self, project_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., vpc_self_link: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., region: _Optional[str] = ..., ip_cidr_range: _Optional[str] = ..., secondary_ip_ranges: _Optional[_Iterable[_Union[GcpSubnetworkSecondaryRange, _Mapping]]] = ..., private_ip_google_access: bool = ...) -> None: ...

class GcpSubnetworkSecondaryRange(_message.Message):
    __slots__ = ("range_name", "ip_cidr_range")
    RANGE_NAME_FIELD_NUMBER: _ClassVar[int]
    IP_CIDR_RANGE_FIELD_NUMBER: _ClassVar[int]
    range_name: str
    ip_cidr_range: str
    def __init__(self, range_name: _Optional[str] = ..., ip_cidr_range: _Optional[str] = ...) -> None: ...
