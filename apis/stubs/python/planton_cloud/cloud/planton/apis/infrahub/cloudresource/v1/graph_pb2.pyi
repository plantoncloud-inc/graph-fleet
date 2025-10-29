from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceGraphView(_message.Message):
    __slots__ = ("org", "env", "nodes", "edges", "topo_order")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    TOPO_ORDER_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    nodes: _containers.RepeatedCompositeFieldContainer[CloudResourceGraphNode]
    edges: _containers.RepeatedCompositeFieldContainer[CloudResourceGraphEdge]
    topo_order: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., nodes: _Optional[_Iterable[_Union[CloudResourceGraphNode, _Mapping]]] = ..., edges: _Optional[_Iterable[_Union[CloudResourceGraphEdge, _Mapping]]] = ..., topo_order: _Optional[_Iterable[str]] = ...) -> None: ...

class CloudResourceGraphNode(_message.Message):
    __slots__ = ("org", "env", "name", "id", "kind")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    name: str
    id: str
    kind: _cloud_resource_kind_pb2.CloudResourceKind
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., name: _Optional[str] = ..., id: _Optional[str] = ..., kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ...) -> None: ...

class CloudResourceGraphEdge(_message.Message):
    __slots__ = ("source_id", "target_id", "source_field_path", "target_field_path")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    target_id: str
    source_field_path: str
    target_field_path: str
    def __init__(self, source_id: _Optional[str] = ..., target_id: _Optional[str] = ..., source_field_path: _Optional[str] = ..., target_field_path: _Optional[str] = ...) -> None: ...

class CloudResourceGraphReference(_message.Message):
    __slots__ = ("source_field_path", "target_field_path", "target")
    SOURCE_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    source_field_path: str
    target_field_path: str
    target: CloudResourceGraphNode
    def __init__(self, source_field_path: _Optional[str] = ..., target_field_path: _Optional[str] = ..., target: _Optional[_Union[CloudResourceGraphNode, _Mapping]] = ...) -> None: ...
