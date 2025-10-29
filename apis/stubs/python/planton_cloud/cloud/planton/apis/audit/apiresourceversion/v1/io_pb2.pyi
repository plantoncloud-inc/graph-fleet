from cloud.planton.apis.audit.apiresourceversion.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceVersionId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class ApiResourceVersionWithContextSizeInput(_message.Message):
    __slots__ = ("version_id", "context_size")
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_SIZE_FIELD_NUMBER: _ClassVar[int]
    version_id: str
    context_size: int
    def __init__(self, version_id: _Optional[str] = ..., context_size: _Optional[int] = ...) -> None: ...

class ListApiResourceVersionsInput(_message.Message):
    __slots__ = ("page_info", "kind", "resource_id")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    kind: _api_resource_kind_pb2.ApiResourceKind
    resource_id: str
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., resource_id: _Optional[str] = ...) -> None: ...

class ApiResourceVersionList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.ApiResourceVersion]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_api_pb2.ApiResourceVersion, _Mapping]]] = ...) -> None: ...

class GetApiResourceVersionCountInput(_message.Message):
    __slots__ = ("kind", "id")
    KIND_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    kind: _api_resource_kind_pb2.ApiResourceKind
    id: str
    def __init__(self, kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., id: _Optional[str] = ...) -> None: ...

class ApiResourceVersionCount(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class ApiResourceCount(_message.Message):
    __slots__ = ("resource_kind", "resource_name", "count")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    resource_kind: str
    resource_name: str
    count: int
    def __init__(self, resource_kind: _Optional[str] = ..., resource_name: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class ApiResourcesCount(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[ApiResourceCount]
    def __init__(self, entries: _Optional[_Iterable[_Union[ApiResourceCount, _Mapping]]] = ...) -> None: ...

class GetResourceCountByOrgRequest(_message.Message):
    __slots__ = ("org",)
    ORG_FIELD_NUMBER: _ClassVar[int]
    org: str
    def __init__(self, org: _Optional[str] = ...) -> None: ...

class GetResourceCountByContextInput(_message.Message):
    __slots__ = ("org", "env")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...
