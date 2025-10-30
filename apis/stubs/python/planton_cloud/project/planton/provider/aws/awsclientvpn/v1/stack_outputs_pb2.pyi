from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsClientVpnStackOutputs(_message.Message):
    __slots__ = ("client_vpn_endpoint_id", "security_group_id", "subnet_association_ids", "endpoint_dns_name")
    class SubnetAssociationIdsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CLIENT_VPN_ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    SUBNET_ASSOCIATION_IDS_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    client_vpn_endpoint_id: str
    security_group_id: str
    subnet_association_ids: _containers.ScalarMap[str, str]
    endpoint_dns_name: str
    def __init__(self, client_vpn_endpoint_id: _Optional[str] = ..., security_group_id: _Optional[str] = ..., subnet_association_ids: _Optional[_Mapping[str, str]] = ..., endpoint_dns_name: _Optional[str] = ...) -> None: ...
