from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_container: _descriptor.FieldDescriptor

class ClickHouseKubernetesSpec(_message.Message):
    __slots__ = ("cluster_name", "container", "ingress", "cluster", "version", "coordination", "zookeeper", "logging")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    COORDINATION_FIELD_NUMBER: _ClassVar[int]
    ZOOKEEPER_FIELD_NUMBER: _ClassVar[int]
    LOGGING_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    container: ClickHouseKubernetesContainer
    ingress: ClickHouseKubernetesIngress
    cluster: ClickHouseKubernetesClusterConfig
    version: str
    coordination: ClickHouseKubernetesCoordinationConfig
    zookeeper: ClickHouseKubernetesZookeeperConfig
    logging: ClickHouseKubernetesLoggingConfig
    def __init__(self, cluster_name: _Optional[str] = ..., container: _Optional[_Union[ClickHouseKubernetesContainer, _Mapping]] = ..., ingress: _Optional[_Union[ClickHouseKubernetesIngress, _Mapping]] = ..., cluster: _Optional[_Union[ClickHouseKubernetesClusterConfig, _Mapping]] = ..., version: _Optional[str] = ..., coordination: _Optional[_Union[ClickHouseKubernetesCoordinationConfig, _Mapping]] = ..., zookeeper: _Optional[_Union[ClickHouseKubernetesZookeeperConfig, _Mapping]] = ..., logging: _Optional[_Union[ClickHouseKubernetesLoggingConfig, _Mapping]] = ...) -> None: ...

class ClickHouseKubernetesContainer(_message.Message):
    __slots__ = ("replicas", "resources", "is_persistence_enabled", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    IS_PERSISTENCE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    is_persistence_enabled: bool
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., is_persistence_enabled: bool = ..., disk_size: _Optional[str] = ...) -> None: ...

class ClickHouseKubernetesClusterConfig(_message.Message):
    __slots__ = ("is_enabled", "shard_count", "replica_count")
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SHARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    is_enabled: bool
    shard_count: int
    replica_count: int
    def __init__(self, is_enabled: bool = ..., shard_count: _Optional[int] = ..., replica_count: _Optional[int] = ...) -> None: ...

class ClickHouseKubernetesCoordinationConfig(_message.Message):
    __slots__ = ("type", "keeper_config", "external_config")
    class CoordinationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        unspecified: _ClassVar[ClickHouseKubernetesCoordinationConfig.CoordinationType]
        keeper: _ClassVar[ClickHouseKubernetesCoordinationConfig.CoordinationType]
        external_keeper: _ClassVar[ClickHouseKubernetesCoordinationConfig.CoordinationType]
        external_zookeeper: _ClassVar[ClickHouseKubernetesCoordinationConfig.CoordinationType]
    unspecified: ClickHouseKubernetesCoordinationConfig.CoordinationType
    keeper: ClickHouseKubernetesCoordinationConfig.CoordinationType
    external_keeper: ClickHouseKubernetesCoordinationConfig.CoordinationType
    external_zookeeper: ClickHouseKubernetesCoordinationConfig.CoordinationType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    KEEPER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CONFIG_FIELD_NUMBER: _ClassVar[int]
    type: ClickHouseKubernetesCoordinationConfig.CoordinationType
    keeper_config: ClickHouseKubernetesKeeperConfig
    external_config: ClickHouseKubernetesExternalCoordinationConfig
    def __init__(self, type: _Optional[_Union[ClickHouseKubernetesCoordinationConfig.CoordinationType, str]] = ..., keeper_config: _Optional[_Union[ClickHouseKubernetesKeeperConfig, _Mapping]] = ..., external_config: _Optional[_Union[ClickHouseKubernetesExternalCoordinationConfig, _Mapping]] = ...) -> None: ...

class ClickHouseKubernetesKeeperConfig(_message.Message):
    __slots__ = ("replicas", "resources", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., disk_size: _Optional[str] = ...) -> None: ...

class ClickHouseKubernetesExternalCoordinationConfig(_message.Message):
    __slots__ = ("nodes",)
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, nodes: _Optional[_Iterable[str]] = ...) -> None: ...

class ClickHouseKubernetesLoggingConfig(_message.Message):
    __slots__ = ("level",)
    class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        information: _ClassVar[ClickHouseKubernetesLoggingConfig.LogLevel]
        debug: _ClassVar[ClickHouseKubernetesLoggingConfig.LogLevel]
        trace: _ClassVar[ClickHouseKubernetesLoggingConfig.LogLevel]
    information: ClickHouseKubernetesLoggingConfig.LogLevel
    debug: ClickHouseKubernetesLoggingConfig.LogLevel
    trace: ClickHouseKubernetesLoggingConfig.LogLevel
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    level: ClickHouseKubernetesLoggingConfig.LogLevel
    def __init__(self, level: _Optional[_Union[ClickHouseKubernetesLoggingConfig.LogLevel, str]] = ...) -> None: ...

class ClickHouseKubernetesIngress(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...

class ClickHouseKubernetesZookeeperConfig(_message.Message):
    __slots__ = ("use_external", "nodes")
    USE_EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    use_external: bool
    nodes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, use_external: bool = ..., nodes: _Optional[_Iterable[str]] = ...) -> None: ...
