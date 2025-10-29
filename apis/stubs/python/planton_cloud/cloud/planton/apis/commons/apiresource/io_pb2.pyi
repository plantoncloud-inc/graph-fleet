from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class ApiResourceDeleteInput(_message.Message):
    __slots__ = ("resource_id", "version_message", "force")
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    resource_id: str
    version_message: str
    force: bool
    def __init__(self, resource_id: _Optional[str] = ..., version_message: _Optional[str] = ..., force: bool = ...) -> None: ...

class ApiResourceKindInput(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _api_resource_kind_pb2.ApiResourceKind
    def __init__(self, value: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ...) -> None: ...

class CloudResourceOwner(_message.Message):
    __slots__ = ("org", "env")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...

class ApiResourceKindAndNameAndId(_message.Message):
    __slots__ = ("kind", "name", "id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    kind: _api_resource_kind_pb2.ApiResourceKind
    name: str
    id: str
    def __init__(self, kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., name: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class ApiResourceByOrgBySlugRequest(_message.Message):
    __slots__ = ("org", "slug")
    ORG_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    org: str
    slug: str
    def __init__(self, org: _Optional[str] = ..., slug: _Optional[str] = ...) -> None: ...

class OrganizationEnvironmentRequest(_message.Message):
    __slots__ = ("org", "env")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...
