from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanKubernetesClusterSpec(_message.Message):
    __slots__ = ("cluster_name", "region", "kubernetes_version", "vpc", "highly_available", "auto_upgrade", "disable_surge_upgrade", "tags", "default_node_pool")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_VERSION_FIELD_NUMBER: _ClassVar[int]
    VPC_FIELD_NUMBER: _ClassVar[int]
    HIGHLY_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    AUTO_UPGRADE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_SURGE_UPGRADE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_NODE_POOL_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    region: _region_pb2.DigitalOceanRegion
    kubernetes_version: str
    vpc: _foreign_key_pb2.StringValueOrRef
    highly_available: bool
    auto_upgrade: bool
    disable_surge_upgrade: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    default_node_pool: DigitalOceanKubernetesClusterDefaultNodePool
    def __init__(self, cluster_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., kubernetes_version: _Optional[str] = ..., vpc: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., highly_available: bool = ..., auto_upgrade: bool = ..., disable_surge_upgrade: bool = ..., tags: _Optional[_Iterable[str]] = ..., default_node_pool: _Optional[_Union[DigitalOceanKubernetesClusterDefaultNodePool, _Mapping]] = ...) -> None: ...

class DigitalOceanKubernetesClusterDefaultNodePool(_message.Message):
    __slots__ = ("size", "node_count", "auto_scale", "min_nodes", "max_nodes")
    SIZE_FIELD_NUMBER: _ClassVar[int]
    NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUTO_SCALE_FIELD_NUMBER: _ClassVar[int]
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    size: str
    node_count: int
    auto_scale: bool
    min_nodes: int
    max_nodes: int
    def __init__(self, size: _Optional[str] = ..., node_count: _Optional[int] = ..., auto_scale: bool = ..., min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ...) -> None: ...
