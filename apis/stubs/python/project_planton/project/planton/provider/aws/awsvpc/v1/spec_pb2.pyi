from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsVpcSpec(_message.Message):
    __slots__ = ("vpc_cidr", "availability_zones", "subnets_per_availability_zone", "subnet_size", "is_nat_gateway_enabled", "is_dns_hostnames_enabled", "is_dns_support_enabled")
    VPC_CIDR_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_ZONES_FIELD_NUMBER: _ClassVar[int]
    SUBNETS_PER_AVAILABILITY_ZONE_FIELD_NUMBER: _ClassVar[int]
    SUBNET_SIZE_FIELD_NUMBER: _ClassVar[int]
    IS_NAT_GATEWAY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_DNS_HOSTNAMES_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_DNS_SUPPORT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    vpc_cidr: str
    availability_zones: _containers.RepeatedScalarFieldContainer[str]
    subnets_per_availability_zone: int
    subnet_size: int
    is_nat_gateway_enabled: bool
    is_dns_hostnames_enabled: bool
    is_dns_support_enabled: bool
    def __init__(self, vpc_cidr: _Optional[str] = ..., availability_zones: _Optional[_Iterable[str]] = ..., subnets_per_availability_zone: _Optional[int] = ..., subnet_size: _Optional[int] = ..., is_nat_gateway_enabled: bool = ..., is_dns_hostnames_enabled: bool = ..., is_dns_support_enabled: bool = ...) -> None: ...
