from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpRouterNatStackOutputs(_message.Message):
    __slots__ = ("name", "router_self_link", "nat_ip_addresses")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROUTER_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    NAT_IP_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    name: str
    router_self_link: str
    nat_ip_addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., router_self_link: _Optional[str] = ..., nat_ip_addresses: _Optional[_Iterable[str]] = ...) -> None: ...
