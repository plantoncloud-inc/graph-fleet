from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.civo import region_pb2 as _region_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CivoLoadBalancerProtocol(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    civo_load_balancer_protocol_unspecified: _ClassVar[CivoLoadBalancerProtocol]
    http: _ClassVar[CivoLoadBalancerProtocol]
    https: _ClassVar[CivoLoadBalancerProtocol]
    tcp: _ClassVar[CivoLoadBalancerProtocol]
civo_load_balancer_protocol_unspecified: CivoLoadBalancerProtocol
http: CivoLoadBalancerProtocol
https: CivoLoadBalancerProtocol
tcp: CivoLoadBalancerProtocol

class CivoLoadBalancerSpec(_message.Message):
    __slots__ = ("load_balancer_name", "region", "network", "forwarding_rules", "health_check", "instance_ids", "instance_tag", "reserved_ip_id", "enable_sticky_sessions")
    LOAD_BALANCER_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    FORWARDING_RULES_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_IDS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TAG_FIELD_NUMBER: _ClassVar[int]
    RESERVED_IP_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLE_STICKY_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    load_balancer_name: str
    region: _region_pb2.CivoRegion
    network: _foreign_key_pb2.StringValueOrRef
    forwarding_rules: _containers.RepeatedCompositeFieldContainer[CivoLoadBalancerForwardingRule]
    health_check: CivoLoadBalancerHealthCheck
    instance_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    instance_tag: str
    reserved_ip_id: _foreign_key_pb2.StringValueOrRef
    enable_sticky_sessions: bool
    def __init__(self, load_balancer_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.CivoRegion, str]] = ..., network: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., forwarding_rules: _Optional[_Iterable[_Union[CivoLoadBalancerForwardingRule, _Mapping]]] = ..., health_check: _Optional[_Union[CivoLoadBalancerHealthCheck, _Mapping]] = ..., instance_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., instance_tag: _Optional[str] = ..., reserved_ip_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., enable_sticky_sessions: bool = ...) -> None: ...

class CivoLoadBalancerForwardingRule(_message.Message):
    __slots__ = ("entry_port", "entry_protocol", "target_port", "target_protocol")
    ENTRY_PORT_FIELD_NUMBER: _ClassVar[int]
    ENTRY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    TARGET_PORT_FIELD_NUMBER: _ClassVar[int]
    TARGET_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    entry_port: int
    entry_protocol: CivoLoadBalancerProtocol
    target_port: int
    target_protocol: CivoLoadBalancerProtocol
    def __init__(self, entry_port: _Optional[int] = ..., entry_protocol: _Optional[_Union[CivoLoadBalancerProtocol, str]] = ..., target_port: _Optional[int] = ..., target_protocol: _Optional[_Union[CivoLoadBalancerProtocol, str]] = ...) -> None: ...

class CivoLoadBalancerHealthCheck(_message.Message):
    __slots__ = ("port", "protocol", "path")
    PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    port: int
    protocol: CivoLoadBalancerProtocol
    path: str
    def __init__(self, port: _Optional[int] = ..., protocol: _Optional[_Union[CivoLoadBalancerProtocol, str]] = ..., path: _Optional[str] = ...) -> None: ...
