from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesWorkloadClusterCredentialAndNamespace(_message.Message):
    __slots__ = ("kubernetes_cluster_credential_id", "kubernetes_namespace")
    KUBERNETES_CLUSTER_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    kubernetes_cluster_credential_id: str
    kubernetes_namespace: str
    def __init__(self, kubernetes_cluster_credential_id: _Optional[str] = ..., kubernetes_namespace: _Optional[str] = ...) -> None: ...
