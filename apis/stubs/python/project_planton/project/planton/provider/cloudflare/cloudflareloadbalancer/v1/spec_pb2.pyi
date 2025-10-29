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

class CloudflareLoadBalancerSessionAffinity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SESSION_AFFINITY_NONE: _ClassVar[CloudflareLoadBalancerSessionAffinity]
    SESSION_AFFINITY_COOKIE: _ClassVar[CloudflareLoadBalancerSessionAffinity]

class CloudflareLoadBalancerSteeringPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEERING_OFF: _ClassVar[CloudflareLoadBalancerSteeringPolicy]
    STEERING_GEO: _ClassVar[CloudflareLoadBalancerSteeringPolicy]
    STEERING_RANDOM: _ClassVar[CloudflareLoadBalancerSteeringPolicy]
SESSION_AFFINITY_NONE: CloudflareLoadBalancerSessionAffinity
SESSION_AFFINITY_COOKIE: CloudflareLoadBalancerSessionAffinity
STEERING_OFF: CloudflareLoadBalancerSteeringPolicy
STEERING_GEO: CloudflareLoadBalancerSteeringPolicy
STEERING_RANDOM: CloudflareLoadBalancerSteeringPolicy

class CloudflareLoadBalancerSpec(_message.Message):
    __slots__ = ("hostname", "zone_id", "origins", "proxied", "health_probe_path", "session_affinity", "steering_policy")
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINS_FIELD_NUMBER: _ClassVar[int]
    PROXIED_FIELD_NUMBER: _ClassVar[int]
    HEALTH_PROBE_PATH_FIELD_NUMBER: _ClassVar[int]
    SESSION_AFFINITY_FIELD_NUMBER: _ClassVar[int]
    STEERING_POLICY_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    zone_id: _foreign_key_pb2.StringValueOrRef
    origins: _containers.RepeatedCompositeFieldContainer[CloudflareLoadBalancerOrigin]
    proxied: bool
    health_probe_path: str
    session_affinity: CloudflareLoadBalancerSessionAffinity
    steering_policy: CloudflareLoadBalancerSteeringPolicy
    def __init__(self, hostname: _Optional[str] = ..., zone_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., origins: _Optional[_Iterable[_Union[CloudflareLoadBalancerOrigin, _Mapping]]] = ..., proxied: bool = ..., health_probe_path: _Optional[str] = ..., session_affinity: _Optional[_Union[CloudflareLoadBalancerSessionAffinity, str]] = ..., steering_policy: _Optional[_Union[CloudflareLoadBalancerSteeringPolicy, str]] = ...) -> None: ...

class CloudflareLoadBalancerOrigin(_message.Message):
    __slots__ = ("name", "address", "weight")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    name: str
    address: str
    weight: int
    def __init__(self, name: _Optional[str] = ..., address: _Optional[str] = ..., weight: _Optional[int] = ...) -> None: ...
