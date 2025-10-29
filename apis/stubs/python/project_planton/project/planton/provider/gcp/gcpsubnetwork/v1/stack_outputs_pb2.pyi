from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpSubnetworkStackOutputs(_message.Message):
    __slots__ = ("subnetwork_self_link", "region", "ip_cidr_range", "secondary_ranges")
    SUBNETWORK_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    IP_CIDR_RANGE_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_RANGES_FIELD_NUMBER: _ClassVar[int]
    subnetwork_self_link: str
    region: str
    ip_cidr_range: str
    secondary_ranges: _containers.RepeatedCompositeFieldContainer[GcpSubnetworkSecondaryRangeStackOutput]
    def __init__(self, subnetwork_self_link: _Optional[str] = ..., region: _Optional[str] = ..., ip_cidr_range: _Optional[str] = ..., secondary_ranges: _Optional[_Iterable[_Union[GcpSubnetworkSecondaryRangeStackOutput, _Mapping]]] = ...) -> None: ...

class GcpSubnetworkSecondaryRangeStackOutput(_message.Message):
    __slots__ = ("range_name", "ip_cidr_range")
    RANGE_NAME_FIELD_NUMBER: _ClassVar[int]
    IP_CIDR_RANGE_FIELD_NUMBER: _ClassVar[int]
    range_name: str
    ip_cidr_range: str
    def __init__(self, range_name: _Optional[str] = ..., ip_cidr_range: _Optional[str] = ...) -> None: ...
