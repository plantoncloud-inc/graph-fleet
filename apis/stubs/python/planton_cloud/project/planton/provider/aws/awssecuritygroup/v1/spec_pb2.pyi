from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsSecurityGroupSpec(_message.Message):
    __slots__ = ("vpc_id", "description", "ingress", "egress")
    VPC_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    EGRESS_FIELD_NUMBER: _ClassVar[int]
    vpc_id: _foreign_key_pb2.StringValueOrRef
    description: str
    ingress: _containers.RepeatedCompositeFieldContainer[SecurityGroupRule]
    egress: _containers.RepeatedCompositeFieldContainer[SecurityGroupRule]
    def __init__(self, vpc_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., description: _Optional[str] = ..., ingress: _Optional[_Iterable[_Union[SecurityGroupRule, _Mapping]]] = ..., egress: _Optional[_Iterable[_Union[SecurityGroupRule, _Mapping]]] = ...) -> None: ...

class SecurityGroupRule(_message.Message):
    __slots__ = ("protocol", "from_port", "to_port", "ipv4_cidrs", "ipv6_cidrs", "source_security_group_ids", "destination_security_group_ids", "self_reference", "description")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    FROM_PORT_FIELD_NUMBER: _ClassVar[int]
    TO_PORT_FIELD_NUMBER: _ClassVar[int]
    IPV4_CIDRS_FIELD_NUMBER: _ClassVar[int]
    IPV6_CIDRS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SECURITY_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_SECURITY_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    SELF_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    from_port: int
    to_port: int
    ipv4_cidrs: _containers.RepeatedScalarFieldContainer[str]
    ipv6_cidrs: _containers.RepeatedScalarFieldContainer[str]
    source_security_group_ids: _containers.RepeatedScalarFieldContainer[str]
    destination_security_group_ids: _containers.RepeatedScalarFieldContainer[str]
    self_reference: bool
    description: str
    def __init__(self, protocol: _Optional[str] = ..., from_port: _Optional[int] = ..., to_port: _Optional[int] = ..., ipv4_cidrs: _Optional[_Iterable[str]] = ..., ipv6_cidrs: _Optional[_Iterable[str]] = ..., source_security_group_ids: _Optional[_Iterable[str]] = ..., destination_security_group_ids: _Optional[_Iterable[str]] = ..., self_reference: bool = ..., description: _Optional[str] = ...) -> None: ...
