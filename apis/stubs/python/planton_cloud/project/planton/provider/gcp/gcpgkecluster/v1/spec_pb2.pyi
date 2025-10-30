from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGkeClusterSpec(_message.Message):
    __slots__ = ("cluster_project_id", "region", "zone", "shared_vpc_config", "is_workload_logs_enabled", "cluster_autoscaling_config", "node_pools")
    CLUSTER_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    SHARED_VPC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    IS_WORKLOAD_LOGS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    NODE_POOLS_FIELD_NUMBER: _ClassVar[int]
    cluster_project_id: str
    region: str
    zone: str
    shared_vpc_config: GcpGkeClusterSharedVpcConfig
    is_workload_logs_enabled: bool
    cluster_autoscaling_config: GcpGkeClusterAutoscalingConfig
    node_pools: _containers.RepeatedCompositeFieldContainer[GcpGkeClusterNodePool]
    def __init__(self, cluster_project_id: _Optional[str] = ..., region: _Optional[str] = ..., zone: _Optional[str] = ..., shared_vpc_config: _Optional[_Union[GcpGkeClusterSharedVpcConfig, _Mapping]] = ..., is_workload_logs_enabled: bool = ..., cluster_autoscaling_config: _Optional[_Union[GcpGkeClusterAutoscalingConfig, _Mapping]] = ..., node_pools: _Optional[_Iterable[_Union[GcpGkeClusterNodePool, _Mapping]]] = ...) -> None: ...

class GcpGkeClusterSharedVpcConfig(_message.Message):
    __slots__ = ("is_enabled", "vpc_project_id")
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    VPC_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    is_enabled: bool
    vpc_project_id: str
    def __init__(self, is_enabled: bool = ..., vpc_project_id: _Optional[str] = ...) -> None: ...

class GcpGkeClusterAutoscalingConfig(_message.Message):
    __slots__ = ("is_enabled", "cpu_min_cores", "cpu_max_cores", "memory_min_gb", "memory_max_gb")
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CPU_MIN_CORES_FIELD_NUMBER: _ClassVar[int]
    CPU_MAX_CORES_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MIN_GB_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MAX_GB_FIELD_NUMBER: _ClassVar[int]
    is_enabled: bool
    cpu_min_cores: int
    cpu_max_cores: int
    memory_min_gb: int
    memory_max_gb: int
    def __init__(self, is_enabled: bool = ..., cpu_min_cores: _Optional[int] = ..., cpu_max_cores: _Optional[int] = ..., memory_min_gb: _Optional[int] = ..., memory_max_gb: _Optional[int] = ...) -> None: ...

class GcpGkeClusterNodePool(_message.Message):
    __slots__ = ("name", "machine_type", "min_node_count", "max_node_count", "is_spot_enabled")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MIN_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    IS_SPOT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    name: str
    machine_type: str
    min_node_count: int
    max_node_count: int
    is_spot_enabled: bool
    def __init__(self, name: _Optional[str] = ..., machine_type: _Optional[str] = ..., min_node_count: _Optional[int] = ..., max_node_count: _Optional[int] = ..., is_spot_enabled: bool = ...) -> None: ...
