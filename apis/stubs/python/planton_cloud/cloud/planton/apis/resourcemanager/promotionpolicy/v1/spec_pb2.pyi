from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PromotionPolicySpec(_message.Message):
    __slots__ = ("selector", "strict", "graph")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    STRICT_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    strict: bool
    graph: PromotionGraph
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., strict: bool = ..., graph: _Optional[_Union[PromotionGraph, _Mapping]] = ...) -> None: ...

class PromotionGraph(_message.Message):
    __slots__ = ("nodes", "edges")
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[EnvironmentNode]
    edges: _containers.RepeatedCompositeFieldContainer[PromotionEdge]
    def __init__(self, nodes: _Optional[_Iterable[_Union[EnvironmentNode, _Mapping]]] = ..., edges: _Optional[_Iterable[_Union[PromotionEdge, _Mapping]]] = ...) -> None: ...

class EnvironmentNode(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class PromotionEdge(_message.Message):
    __slots__ = ("to", "manual_approval")
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    MANUAL_APPROVAL_FIELD_NUMBER: _ClassVar[int]
    to: str
    manual_approval: bool
    def __init__(self, to: _Optional[str] = ..., manual_approval: bool = ..., **kwargs) -> None: ...
