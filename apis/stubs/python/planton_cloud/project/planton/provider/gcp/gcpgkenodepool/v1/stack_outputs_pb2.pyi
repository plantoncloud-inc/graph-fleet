from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGkeNodePoolStackOutputs(_message.Message):
    __slots__ = ("node_pool_name", "instance_group_urls", "min_nodes", "max_nodes", "current_node_count")
    NODE_POOL_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_GROUP_URLS_FIELD_NUMBER: _ClassVar[int]
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    CURRENT_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    node_pool_name: str
    instance_group_urls: _containers.RepeatedScalarFieldContainer[str]
    min_nodes: int
    max_nodes: int
    current_node_count: int
    def __init__(self, node_pool_name: _Optional[str] = ..., instance_group_urls: _Optional[_Iterable[str]] = ..., min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ..., current_node_count: _Optional[int] = ...) -> None: ...
