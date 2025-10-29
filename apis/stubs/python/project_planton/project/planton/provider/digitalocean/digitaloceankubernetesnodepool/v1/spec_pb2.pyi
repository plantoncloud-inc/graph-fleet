from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanKubernetesNodePoolSpec(_message.Message):
    __slots__ = ("node_pool_name", "cluster", "size", "node_count", "auto_scale", "min_nodes", "max_nodes", "tags")
    NODE_POOL_NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUTO_SCALE_FIELD_NUMBER: _ClassVar[int]
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    node_pool_name: str
    cluster: _foreign_key_pb2.StringValueOrRef
    size: str
    node_count: int
    auto_scale: bool
    min_nodes: int
    max_nodes: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, node_pool_name: _Optional[str] = ..., cluster: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., size: _Optional[str] = ..., node_count: _Optional[int] = ..., auto_scale: bool = ..., min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
