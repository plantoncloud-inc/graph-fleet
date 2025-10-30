from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.kubernetes import target_cluster_pb2 as _target_cluster_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExternalDnsKubernetesSpec(_message.Message):
    __slots__ = ("target_cluster", "namespace", "external_dns_version", "helm_chart_version", "gke", "eks", "aks", "cloudflare")
    TARGET_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_DNS_VERSION_FIELD_NUMBER: _ClassVar[int]
    HELM_CHART_VERSION_FIELD_NUMBER: _ClassVar[int]
    GKE_FIELD_NUMBER: _ClassVar[int]
    EKS_FIELD_NUMBER: _ClassVar[int]
    AKS_FIELD_NUMBER: _ClassVar[int]
    CLOUDFLARE_FIELD_NUMBER: _ClassVar[int]
    target_cluster: _target_cluster_pb2.KubernetesAddonTargetCluster
    namespace: str
    external_dns_version: str
    helm_chart_version: str
    gke: ExternalDnsGkeConfig
    eks: ExternalDnsEksConfig
    aks: ExternalDnsAksConfig
    cloudflare: ExternalDnsCloudflareConfig
    def __init__(self, target_cluster: _Optional[_Union[_target_cluster_pb2.KubernetesAddonTargetCluster, _Mapping]] = ..., namespace: _Optional[str] = ..., external_dns_version: _Optional[str] = ..., helm_chart_version: _Optional[str] = ..., gke: _Optional[_Union[ExternalDnsGkeConfig, _Mapping]] = ..., eks: _Optional[_Union[ExternalDnsEksConfig, _Mapping]] = ..., aks: _Optional[_Union[ExternalDnsAksConfig, _Mapping]] = ..., cloudflare: _Optional[_Union[ExternalDnsCloudflareConfig, _Mapping]] = ...) -> None: ...

class ExternalDnsGkeConfig(_message.Message):
    __slots__ = ("project_id", "dns_zone_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DNS_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: _foreign_key_pb2.StringValueOrRef
    dns_zone_id: _foreign_key_pb2.StringValueOrRef
    def __init__(self, project_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., dns_zone_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ...) -> None: ...

class ExternalDnsEksConfig(_message.Message):
    __slots__ = ("route53_zone_id", "irsa_role_arn_override")
    ROUTE53_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    IRSA_ROLE_ARN_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    route53_zone_id: _foreign_key_pb2.StringValueOrRef
    irsa_role_arn_override: str
    def __init__(self, route53_zone_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., irsa_role_arn_override: _Optional[str] = ...) -> None: ...

class ExternalDnsAksConfig(_message.Message):
    __slots__ = ("dns_zone_id", "managed_identity_client_id")
    DNS_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    MANAGED_IDENTITY_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    dns_zone_id: str
    managed_identity_client_id: str
    def __init__(self, dns_zone_id: _Optional[str] = ..., managed_identity_client_id: _Optional[str] = ...) -> None: ...

class ExternalDnsCloudflareConfig(_message.Message):
    __slots__ = ("api_token", "dns_zone_id", "is_proxied")
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DNS_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PROXIED_FIELD_NUMBER: _ClassVar[int]
    api_token: str
    dns_zone_id: str
    is_proxied: bool
    def __init__(self, api_token: _Optional[str] = ..., dns_zone_id: _Optional[str] = ..., is_proxied: bool = ...) -> None: ...
