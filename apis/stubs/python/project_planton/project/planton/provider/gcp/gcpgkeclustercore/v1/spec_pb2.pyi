from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GkeReleaseChannel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    gke_release_channel_unspecified: _ClassVar[GkeReleaseChannel]
    RAPID: _ClassVar[GkeReleaseChannel]
    REGULAR: _ClassVar[GkeReleaseChannel]
    STABLE: _ClassVar[GkeReleaseChannel]
    NONE: _ClassVar[GkeReleaseChannel]
gke_release_channel_unspecified: GkeReleaseChannel
RAPID: GkeReleaseChannel
REGULAR: GkeReleaseChannel
STABLE: GkeReleaseChannel
NONE: GkeReleaseChannel

class GcpGkeClusterCoreSpec(_message.Message):
    __slots__ = ("project_id", "location", "subnetwork_self_link", "cluster_secondary_range_name", "services_secondary_range_name", "master_ipv4_cidr_block", "enable_public_nodes", "release_channel", "disable_network_policy", "disable_workload_identity", "router_nat_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    SUBNETWORK_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_SECONDARY_RANGE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICES_SECONDARY_RANGE_NAME_FIELD_NUMBER: _ClassVar[int]
    MASTER_IPV4_CIDR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PUBLIC_NODES_FIELD_NUMBER: _ClassVar[int]
    RELEASE_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DISABLE_NETWORK_POLICY_FIELD_NUMBER: _ClassVar[int]
    DISABLE_WORKLOAD_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    ROUTER_NAT_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: _foreign_key_pb2.StringValueOrRef
    location: str
    subnetwork_self_link: _foreign_key_pb2.StringValueOrRef
    cluster_secondary_range_name: _foreign_key_pb2.StringValueOrRef
    services_secondary_range_name: _foreign_key_pb2.StringValueOrRef
    master_ipv4_cidr_block: str
    enable_public_nodes: bool
    release_channel: GkeReleaseChannel
    disable_network_policy: bool
    disable_workload_identity: bool
    router_nat_name: _foreign_key_pb2.StringValueOrRef
    def __init__(self, project_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., location: _Optional[str] = ..., subnetwork_self_link: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., cluster_secondary_range_name: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., services_secondary_range_name: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., master_ipv4_cidr_block: _Optional[str] = ..., enable_public_nodes: bool = ..., release_channel: _Optional[_Union[GkeReleaseChannel, str]] = ..., disable_network_policy: bool = ..., disable_workload_identity: bool = ..., router_nat_name: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ...) -> None: ...
