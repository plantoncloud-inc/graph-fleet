from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AzureAksClusterNetworkPlugin(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AZURE_CNI: _ClassVar[AzureAksClusterNetworkPlugin]
    KUBENET: _ClassVar[AzureAksClusterNetworkPlugin]
AZURE_CNI: AzureAksClusterNetworkPlugin
KUBENET: AzureAksClusterNetworkPlugin

class AzureAksClusterSpec(_message.Message):
    __slots__ = ("region", "vnet_subnet_id", "network_plugin", "kubernetes_version", "private_cluster_enabled", "authorized_ip_ranges", "disable_azure_ad_rbac", "log_analytics_workspace_id")
    REGION_FIELD_NUMBER: _ClassVar[int]
    VNET_SUBNET_ID_FIELD_NUMBER: _ClassVar[int]
    NETWORK_PLUGIN_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_VERSION_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_CLUSTER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_IP_RANGES_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AZURE_AD_RBAC_FIELD_NUMBER: _ClassVar[int]
    LOG_ANALYTICS_WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    region: str
    vnet_subnet_id: _foreign_key_pb2.StringValueOrRef
    network_plugin: AzureAksClusterNetworkPlugin
    kubernetes_version: str
    private_cluster_enabled: bool
    authorized_ip_ranges: _containers.RepeatedScalarFieldContainer[str]
    disable_azure_ad_rbac: bool
    log_analytics_workspace_id: str
    def __init__(self, region: _Optional[str] = ..., vnet_subnet_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., network_plugin: _Optional[_Union[AzureAksClusterNetworkPlugin, str]] = ..., kubernetes_version: _Optional[str] = ..., private_cluster_enabled: bool = ..., authorized_ip_ranges: _Optional[_Iterable[str]] = ..., disable_azure_ad_rbac: bool = ..., log_analytics_workspace_id: _Optional[str] = ...) -> None: ...
