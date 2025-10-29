from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AzureNatGatewayStackOutputs(_message.Message):
    __slots__ = ("nat_gateway_id", "public_ip_addresses", "public_ip_prefix_id")
    NAT_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IP_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IP_PREFIX_ID_FIELD_NUMBER: _ClassVar[int]
    nat_gateway_id: str
    public_ip_addresses: _containers.RepeatedScalarFieldContainer[str]
    public_ip_prefix_id: str
    def __init__(self, nat_gateway_id: _Optional[str] = ..., public_ip_addresses: _Optional[_Iterable[str]] = ..., public_ip_prefix_id: _Optional[str] = ...) -> None: ...
