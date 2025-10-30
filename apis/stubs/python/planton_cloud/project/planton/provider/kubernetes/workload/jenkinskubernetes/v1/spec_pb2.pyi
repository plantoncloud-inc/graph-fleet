from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JenkinsKubernetesSpec(_message.Message):
    __slots__ = ("container_resources", "helm_values", "ingress")
    class HelmValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONTAINER_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    HELM_VALUES_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    container_resources: _kubernetes_pb2.ContainerResources
    helm_values: _containers.ScalarMap[str, str]
    ingress: _kubernetes_pb2.IngressSpec
    def __init__(self, container_resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., helm_values: _Optional[_Mapping[str, str]] = ..., ingress: _Optional[_Union[_kubernetes_pb2.IngressSpec, _Mapping]] = ...) -> None: ...
