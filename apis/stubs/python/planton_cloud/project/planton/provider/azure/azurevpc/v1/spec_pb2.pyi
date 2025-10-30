from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AzureVpcSpec(_message.Message):
    __slots__ = ("address_space_cidr", "nodes_subnet_cidr", "is_nat_gateway_enabled", "dns_private_zone_links", "tags")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ADDRESS_SPACE_CIDR_FIELD_NUMBER: _ClassVar[int]
    NODES_SUBNET_CIDR_FIELD_NUMBER: _ClassVar[int]
    IS_NAT_GATEWAY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DNS_PRIVATE_ZONE_LINKS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    address_space_cidr: str
    nodes_subnet_cidr: str
    is_nat_gateway_enabled: bool
    dns_private_zone_links: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.ScalarMap[str, str]
    def __init__(self, address_space_cidr: _Optional[str] = ..., nodes_subnet_cidr: _Optional[str] = ..., is_nat_gateway_enabled: bool = ..., dns_private_zone_links: _Optional[_Iterable[str]] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...
