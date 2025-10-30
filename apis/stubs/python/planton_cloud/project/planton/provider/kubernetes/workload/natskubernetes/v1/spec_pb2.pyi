from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NatsKubernetesAuthScheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    nats_kubernetes_auth_scheme_unspecified: _ClassVar[NatsKubernetesAuthScheme]
    bearer_token: _ClassVar[NatsKubernetesAuthScheme]
    basic_auth: _ClassVar[NatsKubernetesAuthScheme]
nats_kubernetes_auth_scheme_unspecified: NatsKubernetesAuthScheme
bearer_token: NatsKubernetesAuthScheme
basic_auth: NatsKubernetesAuthScheme
DEFAULT_SERVER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_server_container: _descriptor.FieldDescriptor

class NatsKubernetesSpec(_message.Message):
    __slots__ = ("server_container", "disable_jet_stream", "auth", "tls_enabled", "ingress", "disable_nats_box")
    SERVER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    DISABLE_JET_STREAM_FIELD_NUMBER: _ClassVar[int]
    AUTH_FIELD_NUMBER: _ClassVar[int]
    TLS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_NATS_BOX_FIELD_NUMBER: _ClassVar[int]
    server_container: NatsKubernetesServerContainer
    disable_jet_stream: bool
    auth: NatsKubernetesAuth
    tls_enabled: bool
    ingress: NatsKubernetesIngress
    disable_nats_box: bool
    def __init__(self, server_container: _Optional[_Union[NatsKubernetesServerContainer, _Mapping]] = ..., disable_jet_stream: bool = ..., auth: _Optional[_Union[NatsKubernetesAuth, _Mapping]] = ..., tls_enabled: bool = ..., ingress: _Optional[_Union[NatsKubernetesIngress, _Mapping]] = ..., disable_nats_box: bool = ...) -> None: ...

class NatsKubernetesServerContainer(_message.Message):
    __slots__ = ("replicas", "resources", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., disk_size: _Optional[str] = ...) -> None: ...

class NatsKubernetesNoAuthUser(_message.Message):
    __slots__ = ("enabled", "publish_subjects")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_SUBJECTS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    publish_subjects: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, enabled: bool = ..., publish_subjects: _Optional[_Iterable[str]] = ...) -> None: ...

class NatsKubernetesAuth(_message.Message):
    __slots__ = ("enabled", "scheme", "no_auth_user")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    NO_AUTH_USER_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    scheme: NatsKubernetesAuthScheme
    no_auth_user: NatsKubernetesNoAuthUser
    def __init__(self, enabled: bool = ..., scheme: _Optional[_Union[NatsKubernetesAuthScheme, str]] = ..., no_auth_user: _Optional[_Union[NatsKubernetesNoAuthUser, _Mapping]] = ...) -> None: ...

class NatsKubernetesIngress(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...
