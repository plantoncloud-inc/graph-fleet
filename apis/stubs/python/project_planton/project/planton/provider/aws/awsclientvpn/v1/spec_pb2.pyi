from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsClientVpnAuthenticationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    certificate: _ClassVar[AwsClientVpnAuthenticationType]
    directory: _ClassVar[AwsClientVpnAuthenticationType]
    cognito: _ClassVar[AwsClientVpnAuthenticationType]

class AwsClientVpnTransportProtocol(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    aws_client_vpn_transport_protocol_unspecified: _ClassVar[AwsClientVpnTransportProtocol]
    udp: _ClassVar[AwsClientVpnTransportProtocol]
    tcp: _ClassVar[AwsClientVpnTransportProtocol]
certificate: AwsClientVpnAuthenticationType
directory: AwsClientVpnAuthenticationType
cognito: AwsClientVpnAuthenticationType
aws_client_vpn_transport_protocol_unspecified: AwsClientVpnTransportProtocol
udp: AwsClientVpnTransportProtocol
tcp: AwsClientVpnTransportProtocol

class AwsClientVpnSpec(_message.Message):
    __slots__ = ("description", "vpc_id", "subnets", "client_cidr_block", "authentication_type", "server_certificate_arn", "cidr_authorization_rules", "disable_split_tunnel", "vpn_port", "transport_protocol", "log_group_name", "security_groups", "dns_servers")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VPC_ID_FIELD_NUMBER: _ClassVar[int]
    SUBNETS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVER_CERTIFICATE_ARN_FIELD_NUMBER: _ClassVar[int]
    CIDR_AUTHORIZATION_RULES_FIELD_NUMBER: _ClassVar[int]
    DISABLE_SPLIT_TUNNEL_FIELD_NUMBER: _ClassVar[int]
    VPN_PORT_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    LOG_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUPS_FIELD_NUMBER: _ClassVar[int]
    DNS_SERVERS_FIELD_NUMBER: _ClassVar[int]
    description: str
    vpc_id: _foreign_key_pb2.StringValueOrRef
    subnets: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    client_cidr_block: str
    authentication_type: AwsClientVpnAuthenticationType
    server_certificate_arn: _foreign_key_pb2.StringValueOrRef
    cidr_authorization_rules: _containers.RepeatedScalarFieldContainer[str]
    disable_split_tunnel: bool
    vpn_port: int
    transport_protocol: AwsClientVpnTransportProtocol
    log_group_name: str
    security_groups: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    dns_servers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, description: _Optional[str] = ..., vpc_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., subnets: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., client_cidr_block: _Optional[str] = ..., authentication_type: _Optional[_Union[AwsClientVpnAuthenticationType, str]] = ..., server_certificate_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., cidr_authorization_rules: _Optional[_Iterable[str]] = ..., disable_split_tunnel: bool = ..., vpn_port: _Optional[int] = ..., transport_protocol: _Optional[_Union[AwsClientVpnTransportProtocol, str]] = ..., log_group_name: _Optional[str] = ..., security_groups: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., dns_servers: _Optional[_Iterable[str]] = ...) -> None: ...
