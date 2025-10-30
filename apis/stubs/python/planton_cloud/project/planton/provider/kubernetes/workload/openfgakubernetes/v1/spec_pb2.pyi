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

class OpenFgaKubernetesSpec(_message.Message):
    __slots__ = ("container", "ingress", "datastore")
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    DATASTORE_FIELD_NUMBER: _ClassVar[int]
    container: OpenFgaKubernetesContainer
    ingress: OpenFgaKubernetesIngress
    datastore: OpenFgaKubernetesDataStore
    def __init__(self, container: _Optional[_Union[OpenFgaKubernetesContainer, _Mapping]] = ..., ingress: _Optional[_Union[OpenFgaKubernetesIngress, _Mapping]] = ..., datastore: _Optional[_Union[OpenFgaKubernetesDataStore, _Mapping]] = ...) -> None: ...

class OpenFgaKubernetesContainer(_message.Message):
    __slots__ = ("replicas", "resources")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ...) -> None: ...

class OpenFgaKubernetesDataStore(_message.Message):
    __slots__ = ("engine", "uri")
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    engine: str
    uri: str
    def __init__(self, engine: _Optional[str] = ..., uri: _Optional[str] = ...) -> None: ...

class OpenFgaKubernetesIngress(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...
