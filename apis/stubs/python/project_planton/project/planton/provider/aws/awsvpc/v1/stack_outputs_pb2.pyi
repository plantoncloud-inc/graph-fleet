from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsVpcStackOutputs(_message.Message):
    __slots__ = ("vpc_id", "internet_gateway_id", "private_subnets", "public_subnets", "vpc_cidr")
    VPC_ID_FIELD_NUMBER: _ClassVar[int]
    INTERNET_GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_SUBNETS_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_SUBNETS_FIELD_NUMBER: _ClassVar[int]
    VPC_CIDR_FIELD_NUMBER: _ClassVar[int]
    vpc_id: str
    internet_gateway_id: str
    private_subnets: _containers.RepeatedCompositeFieldContainer[AwsVpcSubnetStackOutputs]
    public_subnets: _containers.RepeatedCompositeFieldContainer[AwsVpcSubnetStackOutputs]
    vpc_cidr: str
    def __init__(self, vpc_id: _Optional[str] = ..., internet_gateway_id: _Optional[str] = ..., private_subnets: _Optional[_Iterable[_Union[AwsVpcSubnetStackOutputs, _Mapping]]] = ..., public_subnets: _Optional[_Iterable[_Union[AwsVpcSubnetStackOutputs, _Mapping]]] = ..., vpc_cidr: _Optional[str] = ...) -> None: ...

class AwsVpcSubnetStackOutputs(_message.Message):
    __slots__ = ("name", "id", "cidr", "nat_gateway")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CIDR_FIELD_NUMBER: _ClassVar[int]
    NAT_GATEWAY_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    cidr: str
    nat_gateway: AwsVpcNatGatewayStackOutputs
    def __init__(self, name: _Optional[str] = ..., id: _Optional[str] = ..., cidr: _Optional[str] = ..., nat_gateway: _Optional[_Union[AwsVpcNatGatewayStackOutputs, _Mapping]] = ...) -> None: ...

class AwsVpcNatGatewayStackOutputs(_message.Message):
    __slots__ = ("id", "private_ip", "public_ip")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_IP_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IP_FIELD_NUMBER: _ClassVar[int]
    id: str
    private_ip: str
    public_ip: str
    def __init__(self, id: _Optional[str] = ..., private_ip: _Optional[str] = ..., public_ip: _Optional[str] = ...) -> None: ...
