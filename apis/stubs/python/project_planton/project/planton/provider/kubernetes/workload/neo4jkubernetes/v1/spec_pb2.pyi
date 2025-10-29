from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_container: _descriptor.FieldDescriptor

class Neo4jKubernetesSpec(_message.Message):
    __slots__ = ("container", "memory_config", "ingress")
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    MEMORY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    container: Neo4jKubernetesContainer
    memory_config: Neo4jKubernetesMemoryConfig
    ingress: Neo4jKubernetesIngress
    def __init__(self, container: _Optional[_Union[Neo4jKubernetesContainer, _Mapping]] = ..., memory_config: _Optional[_Union[Neo4jKubernetesMemoryConfig, _Mapping]] = ..., ingress: _Optional[_Union[Neo4jKubernetesIngress, _Mapping]] = ...) -> None: ...

class Neo4jKubernetesContainer(_message.Message):
    __slots__ = ("resources", "persistence_enabled", "disk_size")
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    resources: _kubernetes_pb2.ContainerResources
    persistence_enabled: bool
    disk_size: str
    def __init__(self, resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., persistence_enabled: bool = ..., disk_size: _Optional[str] = ...) -> None: ...

class Neo4jKubernetesMemoryConfig(_message.Message):
    __slots__ = ("heap_max", "page_cache")
    HEAP_MAX_FIELD_NUMBER: _ClassVar[int]
    PAGE_CACHE_FIELD_NUMBER: _ClassVar[int]
    heap_max: str
    page_cache: str
    def __init__(self, heap_max: _Optional[str] = ..., page_cache: _Optional[str] = ...) -> None: ...

class Neo4jKubernetesIngress(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...
