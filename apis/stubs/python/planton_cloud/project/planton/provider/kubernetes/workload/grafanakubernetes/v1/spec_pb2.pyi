from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GrafanaKubernetesSpec(_message.Message):
    __slots__ = ("container", "ingress")
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    container: GrafanaKubernetesSpecContainer
    ingress: _kubernetes_pb2.IngressSpec
    def __init__(self, container: _Optional[_Union[GrafanaKubernetesSpecContainer, _Mapping]] = ..., ingress: _Optional[_Union[_kubernetes_pb2.IngressSpec, _Mapping]] = ...) -> None: ...

class GrafanaKubernetesSpecContainer(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _kubernetes_pb2.ContainerResources
    def __init__(self, resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ...) -> None: ...
