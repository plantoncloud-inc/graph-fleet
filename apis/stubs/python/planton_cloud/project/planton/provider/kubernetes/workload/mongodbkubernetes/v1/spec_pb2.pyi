from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_container: _descriptor.FieldDescriptor

class MongodbKubernetesSpec(_message.Message):
    __slots__ = ("container", "ingress", "helm_values")
    class HelmValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    HELM_VALUES_FIELD_NUMBER: _ClassVar[int]
    container: MongodbKubernetesContainer
    ingress: MongodbKubernetesIngress
    helm_values: _containers.ScalarMap[str, str]
    def __init__(self, container: _Optional[_Union[MongodbKubernetesContainer, _Mapping]] = ..., ingress: _Optional[_Union[MongodbKubernetesIngress, _Mapping]] = ..., helm_values: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MongodbKubernetesIngress(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...

class MongodbKubernetesContainer(_message.Message):
    __slots__ = ("replicas", "resources", "persistence_enabled", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    persistence_enabled: bool
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., persistence_enabled: bool = ..., disk_size: _Optional[str] = ...) -> None: ...
