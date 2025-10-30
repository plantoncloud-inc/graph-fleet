from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanLoadBalancerProtocol(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    digitalocean_load_balancer_protocol_unspecified: _ClassVar[DigitalOceanLoadBalancerProtocol]
    http: _ClassVar[DigitalOceanLoadBalancerProtocol]
    https: _ClassVar[DigitalOceanLoadBalancerProtocol]
    tcp: _ClassVar[DigitalOceanLoadBalancerProtocol]
digitalocean_load_balancer_protocol_unspecified: DigitalOceanLoadBalancerProtocol
http: DigitalOceanLoadBalancerProtocol
https: DigitalOceanLoadBalancerProtocol
tcp: DigitalOceanLoadBalancerProtocol

class DigitalOceanLoadBalancerSpec(_message.Message):
    __slots__ = ("load_balancer_name", "region", "vpc", "forwarding_rules", "health_check", "droplet_ids", "droplet_tag", "enable_sticky_sessions")
    LOAD_BALANCER_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    VPC_FIELD_NUMBER: _ClassVar[int]
    FORWARDING_RULES_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_FIELD_NUMBER: _ClassVar[int]
    DROPLET_IDS_FIELD_NUMBER: _ClassVar[int]
    DROPLET_TAG_FIELD_NUMBER: _ClassVar[int]
    ENABLE_STICKY_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    load_balancer_name: str
    region: _region_pb2.DigitalOceanRegion
    vpc: _foreign_key_pb2.StringValueOrRef
    forwarding_rules: _containers.RepeatedCompositeFieldContainer[DigitalOceanLoadBalancerForwardingRule]
    health_check: DigitalOceanLoadBalancerHealthCheck
    droplet_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    droplet_tag: str
    enable_sticky_sessions: bool
    def __init__(self, load_balancer_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., vpc: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., forwarding_rules: _Optional[_Iterable[_Union[DigitalOceanLoadBalancerForwardingRule, _Mapping]]] = ..., health_check: _Optional[_Union[DigitalOceanLoadBalancerHealthCheck, _Mapping]] = ..., droplet_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., droplet_tag: _Optional[str] = ..., enable_sticky_sessions: bool = ...) -> None: ...

class DigitalOceanLoadBalancerForwardingRule(_message.Message):
    __slots__ = ("entry_port", "entry_protocol", "target_port", "target_protocol")
    ENTRY_PORT_FIELD_NUMBER: _ClassVar[int]
    ENTRY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    TARGET_PORT_FIELD_NUMBER: _ClassVar[int]
    TARGET_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    entry_port: int
    entry_protocol: DigitalOceanLoadBalancerProtocol
    target_port: int
    target_protocol: DigitalOceanLoadBalancerProtocol
    def __init__(self, entry_port: _Optional[int] = ..., entry_protocol: _Optional[_Union[DigitalOceanLoadBalancerProtocol, str]] = ..., target_port: _Optional[int] = ..., target_protocol: _Optional[_Union[DigitalOceanLoadBalancerProtocol, str]] = ...) -> None: ...

class DigitalOceanLoadBalancerHealthCheck(_message.Message):
    __slots__ = ("port", "protocol", "path", "check_interval_sec")
    PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CHECK_INTERVAL_SEC_FIELD_NUMBER: _ClassVar[int]
    port: int
    protocol: DigitalOceanLoadBalancerProtocol
    path: str
    check_interval_sec: int
    def __init__(self, port: _Optional[int] = ..., protocol: _Optional[_Union[DigitalOceanLoadBalancerProtocol, str]] = ..., path: _Optional[str] = ..., check_interval_sec: _Optional[int] = ...) -> None: ...
