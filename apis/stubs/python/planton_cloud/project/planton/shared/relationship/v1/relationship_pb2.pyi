from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceRelationship(_message.Message):
    __slots__ = ("kind", "env", "name", "type", "group")
    class RelationshipType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        unspecified: _ClassVar[CloudResourceRelationship.RelationshipType]
        depends_on: _ClassVar[CloudResourceRelationship.RelationshipType]
        runs_on: _ClassVar[CloudResourceRelationship.RelationshipType]
        managed_by: _ClassVar[CloudResourceRelationship.RelationshipType]
        uses: _ClassVar[CloudResourceRelationship.RelationshipType]
    unspecified: CloudResourceRelationship.RelationshipType
    depends_on: CloudResourceRelationship.RelationshipType
    runs_on: CloudResourceRelationship.RelationshipType
    managed_by: CloudResourceRelationship.RelationshipType
    uses: CloudResourceRelationship.RelationshipType
    KIND_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    kind: _cloud_resource_kind_pb2.CloudResourceKind
    env: str
    name: str
    type: CloudResourceRelationship.RelationshipType
    group: str
    def __init__(self, kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., env: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[CloudResourceRelationship.RelationshipType, str]] = ..., group: _Optional[str] = ...) -> None: ...
