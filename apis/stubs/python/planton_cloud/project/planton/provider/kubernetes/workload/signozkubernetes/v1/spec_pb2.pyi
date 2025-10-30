from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_SIGNOZ_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_signoz_container: _descriptor.FieldDescriptor
DEFAULT_OTEL_COLLECTOR_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_otel_collector_container: _descriptor.FieldDescriptor
DEFAULT_CLICKHOUSE_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_clickhouse_container: _descriptor.FieldDescriptor
DEFAULT_ZOOKEEPER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_zookeeper_container: _descriptor.FieldDescriptor

class SignozKubernetesSpec(_message.Message):
    __slots__ = ("signoz_container", "otel_collector_container", "database", "ingress", "helm_values")
    class HelmValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SIGNOZ_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    OTEL_COLLECTOR_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    HELM_VALUES_FIELD_NUMBER: _ClassVar[int]
    signoz_container: SignozKubernetesContainer
    otel_collector_container: SignozKubernetesContainer
    database: SignozKubernetesDatabaseConfig
    ingress: SignozKubernetesIngress
    helm_values: _containers.ScalarMap[str, str]
    def __init__(self, signoz_container: _Optional[_Union[SignozKubernetesContainer, _Mapping]] = ..., otel_collector_container: _Optional[_Union[SignozKubernetesContainer, _Mapping]] = ..., database: _Optional[_Union[SignozKubernetesDatabaseConfig, _Mapping]] = ..., ingress: _Optional[_Union[SignozKubernetesIngress, _Mapping]] = ..., helm_values: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SignozKubernetesContainer(_message.Message):
    __slots__ = ("replicas", "resources", "image")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    image: _kubernetes_pb2.ContainerImage
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., image: _Optional[_Union[_kubernetes_pb2.ContainerImage, _Mapping]] = ...) -> None: ...

class SignozKubernetesDatabaseConfig(_message.Message):
    __slots__ = ("is_external", "external_database", "managed_database")
    IS_EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_DATABASE_FIELD_NUMBER: _ClassVar[int]
    MANAGED_DATABASE_FIELD_NUMBER: _ClassVar[int]
    is_external: bool
    external_database: SignozKubernetesExternalClickhouse
    managed_database: SignozKubernetesManagedClickhouse
    def __init__(self, is_external: bool = ..., external_database: _Optional[_Union[SignozKubernetesExternalClickhouse, _Mapping]] = ..., managed_database: _Optional[_Union[SignozKubernetesManagedClickhouse, _Mapping]] = ...) -> None: ...

class SignozKubernetesExternalClickhouse(_message.Message):
    __slots__ = ("host", "http_port", "tcp_port", "cluster_name", "is_secure", "username", "password")
    HOST_FIELD_NUMBER: _ClassVar[int]
    HTTP_PORT_FIELD_NUMBER: _ClassVar[int]
    TCP_PORT_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_SECURE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    host: str
    http_port: int
    tcp_port: int
    cluster_name: str
    is_secure: bool
    username: str
    password: str
    def __init__(self, host: _Optional[str] = ..., http_port: _Optional[int] = ..., tcp_port: _Optional[int] = ..., cluster_name: _Optional[str] = ..., is_secure: bool = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class SignozKubernetesManagedClickhouse(_message.Message):
    __slots__ = ("container", "cluster", "zookeeper")
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    ZOOKEEPER_FIELD_NUMBER: _ClassVar[int]
    container: SignozKubernetesClickhouseContainer
    cluster: SignozKubernetesClickhouseCluster
    zookeeper: SignozKubernetesZookeeperConfig
    def __init__(self, container: _Optional[_Union[SignozKubernetesClickhouseContainer, _Mapping]] = ..., cluster: _Optional[_Union[SignozKubernetesClickhouseCluster, _Mapping]] = ..., zookeeper: _Optional[_Union[SignozKubernetesZookeeperConfig, _Mapping]] = ...) -> None: ...

class SignozKubernetesClickhouseContainer(_message.Message):
    __slots__ = ("replicas", "resources", "image", "is_persistence_enabled", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    IS_PERSISTENCE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    image: _kubernetes_pb2.ContainerImage
    is_persistence_enabled: bool
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., image: _Optional[_Union[_kubernetes_pb2.ContainerImage, _Mapping]] = ..., is_persistence_enabled: bool = ..., disk_size: _Optional[str] = ...) -> None: ...

class SignozKubernetesClickhouseCluster(_message.Message):
    __slots__ = ("is_enabled", "shard_count", "replica_count")
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SHARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    is_enabled: bool
    shard_count: int
    replica_count: int
    def __init__(self, is_enabled: bool = ..., shard_count: _Optional[int] = ..., replica_count: _Optional[int] = ...) -> None: ...

class SignozKubernetesZookeeperConfig(_message.Message):
    __slots__ = ("is_enabled", "container")
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    is_enabled: bool
    container: SignozKubernetesZookeeperContainer
    def __init__(self, is_enabled: bool = ..., container: _Optional[_Union[SignozKubernetesZookeeperContainer, _Mapping]] = ...) -> None: ...

class SignozKubernetesZookeeperContainer(_message.Message):
    __slots__ = ("replicas", "resources", "image", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    image: _kubernetes_pb2.ContainerImage
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., image: _Optional[_Union[_kubernetes_pb2.ContainerImage, _Mapping]] = ..., disk_size: _Optional[str] = ...) -> None: ...

class SignozKubernetesIngress(_message.Message):
    __slots__ = ("ui", "otel_collector")
    UI_FIELD_NUMBER: _ClassVar[int]
    OTEL_COLLECTOR_FIELD_NUMBER: _ClassVar[int]
    ui: SignozKubernetesIngressEndpoint
    otel_collector: SignozKubernetesIngressEndpoint
    def __init__(self, ui: _Optional[_Union[SignozKubernetesIngressEndpoint, _Mapping]] = ..., otel_collector: _Optional[_Union[SignozKubernetesIngressEndpoint, _Mapping]] = ...) -> None: ...

class SignozKubernetesIngressEndpoint(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...
