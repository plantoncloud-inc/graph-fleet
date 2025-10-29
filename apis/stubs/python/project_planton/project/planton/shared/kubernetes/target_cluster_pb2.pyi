from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesAddonTargetCluster(_message.Message):
    __slots__ = ("kubernetes_cluster_credential_id", "kubernetes_cluster_selector")
    KUBERNETES_CLUSTER_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_CLUSTER_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    kubernetes_cluster_credential_id: str
    kubernetes_cluster_selector: KubernetesClusterCloudResourceSelector
    def __init__(self, kubernetes_cluster_credential_id: _Optional[str] = ..., kubernetes_cluster_selector: _Optional[_Union[KubernetesClusterCloudResourceSelector, _Mapping]] = ...) -> None: ...

class KubernetesClusterCloudResourceSelector(_message.Message):
    __slots__ = ("cluster_kind", "cluster_name")
    CLUSTER_KIND_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    cluster_kind: _cloud_resource_kind_pb2.CloudResourceKind
    cluster_name: str
    def __init__(self, cluster_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., cluster_name: _Optional[str] = ...) -> None: ...
