from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from project.planton.shared.kubernetes import target_cluster_pb2 as _target_cluster_pb2
from project.planton.shared.options import options_pb2 as _options_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExternalSecretsKubernetesSpec(_message.Message):
    __slots__ = ("target_cluster", "poll_interval_seconds", "container", "gke", "eks", "aks")
    TARGET_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    POLL_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    GKE_FIELD_NUMBER: _ClassVar[int]
    EKS_FIELD_NUMBER: _ClassVar[int]
    AKS_FIELD_NUMBER: _ClassVar[int]
    target_cluster: _target_cluster_pb2.KubernetesAddonTargetCluster
    poll_interval_seconds: int
    container: ExternalSecretsKubernetesSpecContainer
    gke: ExternalSecretsGkeConfig
    eks: ExternalSecretsEksConfig
    aks: ExternalSecretsAksConfig
    def __init__(self, target_cluster: _Optional[_Union[_target_cluster_pb2.KubernetesAddonTargetCluster, _Mapping]] = ..., poll_interval_seconds: _Optional[int] = ..., container: _Optional[_Union[ExternalSecretsKubernetesSpecContainer, _Mapping]] = ..., gke: _Optional[_Union[ExternalSecretsGkeConfig, _Mapping]] = ..., eks: _Optional[_Union[ExternalSecretsEksConfig, _Mapping]] = ..., aks: _Optional[_Union[ExternalSecretsAksConfig, _Mapping]] = ...) -> None: ...

class ExternalSecretsKubernetesSpecContainer(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _kubernetes_pb2.ContainerResources
    def __init__(self, resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ...) -> None: ...

class ExternalSecretsGkeConfig(_message.Message):
    __slots__ = ("project_id", "gsa_email")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    GSA_EMAIL_FIELD_NUMBER: _ClassVar[int]
    project_id: _foreign_key_pb2.StringValueOrRef
    gsa_email: str
    def __init__(self, project_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., gsa_email: _Optional[str] = ...) -> None: ...

class ExternalSecretsEksConfig(_message.Message):
    __slots__ = ("region", "irsa_role_arn_override")
    REGION_FIELD_NUMBER: _ClassVar[int]
    IRSA_ROLE_ARN_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    region: str
    irsa_role_arn_override: str
    def __init__(self, region: _Optional[str] = ..., irsa_role_arn_override: _Optional[str] = ...) -> None: ...

class ExternalSecretsAksConfig(_message.Message):
    __slots__ = ("key_vault_resource_id", "managed_identity_client_id")
    KEY_VAULT_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    MANAGED_IDENTITY_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    key_vault_resource_id: str
    managed_identity_client_id: str
    def __init__(self, key_vault_resource_id: _Optional[str] = ..., managed_identity_client_id: _Optional[str] = ...) -> None: ...
