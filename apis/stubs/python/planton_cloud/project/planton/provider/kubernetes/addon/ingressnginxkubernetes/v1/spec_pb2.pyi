from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.kubernetes import target_cluster_pb2 as _target_cluster_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IngressNginxKubernetesSpec(_message.Message):
    __slots__ = ("target_cluster", "chart_version", "internal", "gke", "eks", "aks")
    TARGET_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    CHART_VERSION_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    GKE_FIELD_NUMBER: _ClassVar[int]
    EKS_FIELD_NUMBER: _ClassVar[int]
    AKS_FIELD_NUMBER: _ClassVar[int]
    target_cluster: _target_cluster_pb2.KubernetesAddonTargetCluster
    chart_version: str
    internal: bool
    gke: IngressNginxGkeConfig
    eks: IngressNginxEksConfig
    aks: IngressNginxAksConfig
    def __init__(self, target_cluster: _Optional[_Union[_target_cluster_pb2.KubernetesAddonTargetCluster, _Mapping]] = ..., chart_version: _Optional[str] = ..., internal: bool = ..., gke: _Optional[_Union[IngressNginxGkeConfig, _Mapping]] = ..., eks: _Optional[_Union[IngressNginxEksConfig, _Mapping]] = ..., aks: _Optional[_Union[IngressNginxAksConfig, _Mapping]] = ...) -> None: ...

class IngressNginxGkeConfig(_message.Message):
    __slots__ = ("static_ip_name", "subnetwork_self_link")
    STATIC_IP_NAME_FIELD_NUMBER: _ClassVar[int]
    SUBNETWORK_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    static_ip_name: str
    subnetwork_self_link: str
    def __init__(self, static_ip_name: _Optional[str] = ..., subnetwork_self_link: _Optional[str] = ...) -> None: ...

class IngressNginxEksConfig(_message.Message):
    __slots__ = ("additional_security_group_ids", "subnet_ids", "irsa_role_arn_override")
    ADDITIONAL_SECURITY_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    SUBNET_IDS_FIELD_NUMBER: _ClassVar[int]
    IRSA_ROLE_ARN_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    additional_security_group_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    subnet_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    irsa_role_arn_override: str
    def __init__(self, additional_security_group_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., subnet_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., irsa_role_arn_override: _Optional[str] = ...) -> None: ...

class IngressNginxAksConfig(_message.Message):
    __slots__ = ("managed_identity_client_id", "public_ip_name")
    MANAGED_IDENTITY_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IP_NAME_FIELD_NUMBER: _ClassVar[int]
    managed_identity_client_id: str
    public_ip_name: str
    def __init__(self, managed_identity_client_id: _Optional[str] = ..., public_ip_name: _Optional[str] = ...) -> None: ...
