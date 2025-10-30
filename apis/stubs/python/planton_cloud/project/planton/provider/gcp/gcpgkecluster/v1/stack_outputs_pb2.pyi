from project.planton.shared.gcp import gcp_pb2 as _gcp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGkeClusterStackOutputs(_message.Message):
    __slots__ = ("cluster_endpoint", "cluster_ca_data", "external_nat_ip", "gke_webhooks_firewall_self_link", "network_self_link", "sub_network_self_link", "router_nat_name", "router_self_link", "workload_deployer_service_account")
    CLUSTER_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CA_DATA_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_NAT_IP_FIELD_NUMBER: _ClassVar[int]
    GKE_WEBHOOKS_FIREWALL_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    NETWORK_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    SUB_NETWORK_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    ROUTER_NAT_NAME_FIELD_NUMBER: _ClassVar[int]
    ROUTER_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_DEPLOYER_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    cluster_endpoint: str
    cluster_ca_data: str
    external_nat_ip: str
    gke_webhooks_firewall_self_link: str
    network_self_link: str
    sub_network_self_link: str
    router_nat_name: str
    router_self_link: str
    workload_deployer_service_account: _gcp_pb2.GoogleServiceAccount
    def __init__(self, cluster_endpoint: _Optional[str] = ..., cluster_ca_data: _Optional[str] = ..., external_nat_ip: _Optional[str] = ..., gke_webhooks_firewall_self_link: _Optional[str] = ..., network_self_link: _Optional[str] = ..., sub_network_self_link: _Optional[str] = ..., router_nat_name: _Optional[str] = ..., router_self_link: _Optional[str] = ..., workload_deployer_service_account: _Optional[_Union[_gcp_pb2.GoogleServiceAccount, _Mapping]] = ...) -> None: ...
