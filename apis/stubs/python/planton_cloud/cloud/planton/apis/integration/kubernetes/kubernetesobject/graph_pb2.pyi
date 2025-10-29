from cloud.planton.apis.integration.kubernetes.kubernetesobject import kind_pb2 as _kind_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesObjectGraphEdgeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    kubernetes_object_graph_edge_type_unspecified: _ClassVar[KubernetesObjectGraphEdgeType]
    owns: _ClassVar[KubernetesObjectGraphEdgeType]
    selects: _ClassVar[KubernetesObjectGraphEdgeType]
    mounts: _ClassVar[KubernetesObjectGraphEdgeType]
kubernetes_object_graph_edge_type_unspecified: KubernetesObjectGraphEdgeType
owns: KubernetesObjectGraphEdgeType
selects: KubernetesObjectGraphEdgeType
mounts: KubernetesObjectGraphEdgeType

class KubernetesObjectGraphNode(_message.Message):
    __slots__ = ("uid", "api_version", "kind", "namespace", "name", "icon_url")
    UID_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    uid: str
    api_version: str
    kind: _kind_pb2.KubernetesObjectKind
    namespace: str
    name: str
    icon_url: str
    def __init__(self, uid: _Optional[str] = ..., api_version: _Optional[str] = ..., kind: _Optional[_Union[_kind_pb2.KubernetesObjectKind, str]] = ..., namespace: _Optional[str] = ..., name: _Optional[str] = ..., icon_url: _Optional[str] = ...) -> None: ...

class KubernetesObjectGraphEdge(_message.Message):
    __slots__ = ("from_uid", "to_uid", "type")
    FROM_UID_FIELD_NUMBER: _ClassVar[int]
    TO_UID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    from_uid: str
    to_uid: str
    type: KubernetesObjectGraphEdgeType
    def __init__(self, from_uid: _Optional[str] = ..., to_uid: _Optional[str] = ..., type: _Optional[_Union[KubernetesObjectGraphEdgeType, str]] = ...) -> None: ...

class KubernetesObjectGraphSnapshot(_message.Message):
    __slots__ = ("nodes", "edges", "complete")
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[KubernetesObjectGraphNode]
    edges: _containers.RepeatedCompositeFieldContainer[KubernetesObjectGraphEdge]
    complete: bool
    def __init__(self, nodes: _Optional[_Iterable[_Union[KubernetesObjectGraphNode, _Mapping]]] = ..., edges: _Optional[_Iterable[_Union[KubernetesObjectGraphEdge, _Mapping]]] = ..., complete: bool = ...) -> None: ...
