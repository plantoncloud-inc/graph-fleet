from project.planton.shared.relationship.v1 import relationship_pb2 as _relationship_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceMetadata(_message.Message):
    __slots__ = ("name", "slug", "id", "org", "env", "labels", "annotations", "tags", "relationships")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    RELATIONSHIPS_FIELD_NUMBER: _ClassVar[int]
    name: str
    slug: str
    id: str
    org: str
    env: str
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    tags: _containers.RepeatedScalarFieldContainer[str]
    relationships: _containers.RepeatedCompositeFieldContainer[_relationship_pb2.CloudResourceRelationship]
    def __init__(self, name: _Optional[str] = ..., slug: _Optional[str] = ..., id: _Optional[str] = ..., org: _Optional[str] = ..., env: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ..., annotations: _Optional[_Mapping[str, str]] = ..., tags: _Optional[_Iterable[str]] = ..., relationships: _Optional[_Iterable[_Union[_relationship_pb2.CloudResourceRelationship, _Mapping]]] = ...) -> None: ...
