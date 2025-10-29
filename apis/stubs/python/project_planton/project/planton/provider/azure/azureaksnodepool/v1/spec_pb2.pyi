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

class AzureAksNodePoolOsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    azure_aks_node_pool_os_type_unspecified: _ClassVar[AzureAksNodePoolOsType]
    LINUX: _ClassVar[AzureAksNodePoolOsType]
    WINDOWS: _ClassVar[AzureAksNodePoolOsType]
azure_aks_node_pool_os_type_unspecified: AzureAksNodePoolOsType
LINUX: AzureAksNodePoolOsType
WINDOWS: AzureAksNodePoolOsType

class AzureAksNodePoolSpec(_message.Message):
    __slots__ = ("cluster_name", "vm_size", "initial_node_count", "autoscaling", "availability_zones", "os_type", "spot_enabled")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    VM_SIZE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_ZONES_FIELD_NUMBER: _ClassVar[int]
    OS_TYPE_FIELD_NUMBER: _ClassVar[int]
    SPOT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    cluster_name: _foreign_key_pb2.StringValueOrRef
    vm_size: str
    initial_node_count: int
    autoscaling: AzureAksNodePoolAutoscaling
    availability_zones: _containers.RepeatedScalarFieldContainer[str]
    os_type: AzureAksNodePoolOsType
    spot_enabled: bool
    def __init__(self, cluster_name: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., vm_size: _Optional[str] = ..., initial_node_count: _Optional[int] = ..., autoscaling: _Optional[_Union[AzureAksNodePoolAutoscaling, _Mapping]] = ..., availability_zones: _Optional[_Iterable[str]] = ..., os_type: _Optional[_Union[AzureAksNodePoolOsType, str]] = ..., spot_enabled: bool = ...) -> None: ...

class AzureAksNodePoolAutoscaling(_message.Message):
    __slots__ = ("min_nodes", "max_nodes")
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    min_nodes: int
    max_nodes: int
    def __init__(self, min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ...) -> None: ...
