from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    kubernetes_provider_unspecified: _ClassVar[KubernetesProvider]
    gcp_gke: _ClassVar[KubernetesProvider]
    aws_eks: _ClassVar[KubernetesProvider]
    azure_aks: _ClassVar[KubernetesProvider]
    digital_ocean_doks: _ClassVar[KubernetesProvider]
kubernetes_provider_unspecified: KubernetesProvider
gcp_gke: KubernetesProvider
aws_eks: KubernetesProvider
azure_aks: KubernetesProvider
digital_ocean_doks: KubernetesProvider

class KubernetesProviderConfig(_message.Message):
    __slots__ = ("provider", "gcp_gke", "aws_eks", "azure_aks", "digital_ocean_doks")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GCP_GKE_FIELD_NUMBER: _ClassVar[int]
    AWS_EKS_FIELD_NUMBER: _ClassVar[int]
    AZURE_AKS_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_OCEAN_DOKS_FIELD_NUMBER: _ClassVar[int]
    provider: KubernetesProvider
    gcp_gke: KubernetesProviderConfigGcpGke
    aws_eks: KubernetesProviderConfigAwsEks
    azure_aks: KubernetesProviderConfigAzureAks
    digital_ocean_doks: KubernetesProviderConfigDigitalOceanDoks
    def __init__(self, provider: _Optional[_Union[KubernetesProvider, str]] = ..., gcp_gke: _Optional[_Union[KubernetesProviderConfigGcpGke, _Mapping]] = ..., aws_eks: _Optional[_Union[KubernetesProviderConfigAwsEks, _Mapping]] = ..., azure_aks: _Optional[_Union[KubernetesProviderConfigAzureAks, _Mapping]] = ..., digital_ocean_doks: _Optional[_Union[KubernetesProviderConfigDigitalOceanDoks, _Mapping]] = ...) -> None: ...

class KubernetesProviderConfigGcpGke(_message.Message):
    __slots__ = ("cluster_endpoint", "cluster_ca_data", "service_account_key_base64")
    CLUSTER_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CA_DATA_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    cluster_endpoint: str
    cluster_ca_data: str
    service_account_key_base64: str
    def __init__(self, cluster_endpoint: _Optional[str] = ..., cluster_ca_data: _Optional[str] = ..., service_account_key_base64: _Optional[str] = ...) -> None: ...

class KubernetesProviderConfigAwsEks(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class KubernetesProviderConfigAzureAks(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class KubernetesProviderConfigDigitalOceanDoks(_message.Message):
    __slots__ = ("kube_config",)
    KUBE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    kube_config: str
    def __init__(self, kube_config: _Optional[str] = ...) -> None: ...
