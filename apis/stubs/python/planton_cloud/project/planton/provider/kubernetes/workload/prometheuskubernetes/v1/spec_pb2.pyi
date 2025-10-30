from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from project.planton.shared.options import options_pb2 as _options_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PrometheusKubernetesSpec(_message.Message):
    __slots__ = ("container", "ingress")
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    container: PrometheusKubernetesContainer
    ingress: _kubernetes_pb2.IngressSpec
    def __init__(self, container: _Optional[_Union[PrometheusKubernetesContainer, _Mapping]] = ..., ingress: _Optional[_Union[_kubernetes_pb2.IngressSpec, _Mapping]] = ...) -> None: ...

class PrometheusKubernetesContainer(_message.Message):
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
