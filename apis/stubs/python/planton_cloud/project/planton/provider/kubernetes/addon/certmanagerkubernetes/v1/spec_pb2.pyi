from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.kubernetes import target_cluster_pb2 as _target_cluster_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CertManagerKubernetesSpec(_message.Message):
    __slots__ = ("target_cluster", "release_channel", "skip_install_self_signed_issuer", "gke", "eks", "aks")
    TARGET_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    RELEASE_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    SKIP_INSTALL_SELF_SIGNED_ISSUER_FIELD_NUMBER: _ClassVar[int]
    GKE_FIELD_NUMBER: _ClassVar[int]
    EKS_FIELD_NUMBER: _ClassVar[int]
    AKS_FIELD_NUMBER: _ClassVar[int]
    target_cluster: _target_cluster_pb2.KubernetesAddonTargetCluster
    release_channel: str
    skip_install_self_signed_issuer: bool
    gke: CertManagerGkeConfig
    eks: CertManagerEksConfig
    aks: CertManagerAksConfig
    def __init__(self, target_cluster: _Optional[_Union[_target_cluster_pb2.KubernetesAddonTargetCluster, _Mapping]] = ..., release_channel: _Optional[str] = ..., skip_install_self_signed_issuer: bool = ..., gke: _Optional[_Union[CertManagerGkeConfig, _Mapping]] = ..., eks: _Optional[_Union[CertManagerEksConfig, _Mapping]] = ..., aks: _Optional[_Union[CertManagerAksConfig, _Mapping]] = ...) -> None: ...

class CertManagerGkeConfig(_message.Message):
    __slots__ = ("project_id", "dns_zone_id", "gsa_email")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DNS_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    GSA_EMAIL_FIELD_NUMBER: _ClassVar[int]
    project_id: _foreign_key_pb2.StringValueOrRef
    dns_zone_id: _foreign_key_pb2.StringValueOrRef
    gsa_email: str
    def __init__(self, project_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., dns_zone_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., gsa_email: _Optional[str] = ...) -> None: ...

class CertManagerEksConfig(_message.Message):
    __slots__ = ("route53_zone_id", "irsa_role_arn_override")
    ROUTE53_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    IRSA_ROLE_ARN_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    route53_zone_id: _foreign_key_pb2.StringValueOrRef
    irsa_role_arn_override: str
    def __init__(self, route53_zone_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., irsa_role_arn_override: _Optional[str] = ...) -> None: ...

class CertManagerAksConfig(_message.Message):
    __slots__ = ("dns_zone_id", "managed_identity_client_id")
    DNS_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    MANAGED_IDENTITY_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    dns_zone_id: str
    managed_identity_client_id: str
    def __init__(self, dns_zone_id: _Optional[str] = ..., managed_identity_client_id: _Optional[str] = ...) -> None: ...
