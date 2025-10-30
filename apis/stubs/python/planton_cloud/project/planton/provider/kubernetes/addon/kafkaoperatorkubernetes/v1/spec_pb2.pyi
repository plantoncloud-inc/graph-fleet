from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from project.planton.shared.kubernetes import target_cluster_pb2 as _target_cluster_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KafkaOperatorKubernetesSpec(_message.Message):
    __slots__ = ("target_cluster", "container")
    TARGET_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    target_cluster: _target_cluster_pb2.KubernetesAddonTargetCluster
    container: KafkaOperatorKubernetesSpecContainer
    def __init__(self, target_cluster: _Optional[_Union[_target_cluster_pb2.KubernetesAddonTargetCluster, _Mapping]] = ..., container: _Optional[_Union[KafkaOperatorKubernetesSpecContainer, _Mapping]] = ...) -> None: ...

class KafkaOperatorKubernetesSpecContainer(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _kubernetes_pb2.ContainerResources
    def __init__(self, resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ...) -> None: ...
