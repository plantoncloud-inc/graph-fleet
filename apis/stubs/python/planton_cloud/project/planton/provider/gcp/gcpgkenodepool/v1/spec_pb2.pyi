from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGkeNodePoolSpec(_message.Message):
    __slots__ = ("cluster_project_id", "cluster_name", "machine_type", "disk_size_gb", "disk_type", "image_type", "service_account", "management", "spot", "node_labels", "node_count", "autoscaling")
    class NodeLabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CLUSTER_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_GB_FIELD_NUMBER: _ClassVar[int]
    DISK_TYPE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    SPOT_FIELD_NUMBER: _ClassVar[int]
    NODE_LABELS_FIELD_NUMBER: _ClassVar[int]
    NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_FIELD_NUMBER: _ClassVar[int]
    cluster_project_id: _foreign_key_pb2.StringValueOrRef
    cluster_name: _foreign_key_pb2.StringValueOrRef
    machine_type: str
    disk_size_gb: int
    disk_type: str
    image_type: str
    service_account: str
    management: GcpGkeClusterNodePoolNodeManagement
    spot: bool
    node_labels: _containers.ScalarMap[str, str]
    node_count: int
    autoscaling: GcpGkeNodePoolAutoscaling
    def __init__(self, cluster_project_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., cluster_name: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., machine_type: _Optional[str] = ..., disk_size_gb: _Optional[int] = ..., disk_type: _Optional[str] = ..., image_type: _Optional[str] = ..., service_account: _Optional[str] = ..., management: _Optional[_Union[GcpGkeClusterNodePoolNodeManagement, _Mapping]] = ..., spot: bool = ..., node_labels: _Optional[_Mapping[str, str]] = ..., node_count: _Optional[int] = ..., autoscaling: _Optional[_Union[GcpGkeNodePoolAutoscaling, _Mapping]] = ...) -> None: ...

class GcpGkeNodePoolAutoscaling(_message.Message):
    __slots__ = ("min_nodes", "max_nodes", "location_policy")
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    LOCATION_POLICY_FIELD_NUMBER: _ClassVar[int]
    min_nodes: int
    max_nodes: int
    location_policy: str
    def __init__(self, min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ..., location_policy: _Optional[str] = ...) -> None: ...

class GcpGkeClusterNodePoolNodeManagement(_message.Message):
    __slots__ = ("disable_auto_upgrade", "disable_auto_repair")
    DISABLE_AUTO_UPGRADE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AUTO_REPAIR_FIELD_NUMBER: _ClassVar[int]
    disable_auto_upgrade: bool
    disable_auto_repair: bool
    def __init__(self, disable_auto_upgrade: bool = ..., disable_auto_repair: bool = ...) -> None: ...
