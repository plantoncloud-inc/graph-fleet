from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Team(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.ApiResourceMetadata
    spec: TeamSpec
    status: _status_pb2.ApiResourceAuditStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[TeamSpec, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.ApiResourceAuditStatus, _Mapping]] = ...) -> None: ...

class TeamSpec(_message.Message):
    __slots__ = ("description", "members")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    description: str
    members: _containers.RepeatedCompositeFieldContainer[TeamMember]
    def __init__(self, description: _Optional[str] = ..., members: _Optional[_Iterable[_Union[TeamMember, _Mapping]]] = ...) -> None: ...

class TeamMember(_message.Message):
    __slots__ = ("member_type", "member_id", "email", "name", "avatar", "slug")
    MEMBER_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    member_type: _api_resource_kind_pb2.ApiResourceKind
    member_id: str
    email: str
    name: str
    avatar: str
    slug: str
    def __init__(self, member_type: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., member_id: _Optional[str] = ..., email: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., slug: _Optional[str] = ...) -> None: ...
