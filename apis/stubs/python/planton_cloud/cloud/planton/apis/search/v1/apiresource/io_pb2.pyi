from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from cloud.planton.apis.search.v1.apiresource import record_pb2 as _record_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceSearchRecords(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_record_pb2.ApiResourceSearchRecord]
    def __init__(self, entries: _Optional[_Iterable[_Union[_record_pb2.ApiResourceSearchRecord, _Mapping]]] = ...) -> None: ...

class ApiResourceSearchRecordList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_record_pb2.ApiResourceSearchRecord]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_record_pb2.ApiResourceSearchRecord, _Mapping]]] = ...) -> None: ...

class SearchByTextInput(_message.Message):
    __slots__ = ("org", "env", "search_text", "page_info")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    search_text: str
    page_info: _pagination_pb2.PageInfo
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ...) -> None: ...

class SearchApiResourcesByKindInput(_message.Message):
    __slots__ = ("org", "env", "api_resource_kind", "page_info", "search_text")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    page_info: _pagination_pb2.PageInfo
    search_text: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., search_text: _Optional[str] = ...) -> None: ...

class GetByOrgByKindByNameRequest(_message.Message):
    __slots__ = ("org", "api_resource_kind", "name")
    ORG_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    org: str
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    name: str
    def __init__(self, org: _Optional[str] = ..., api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., name: _Optional[str] = ...) -> None: ...

class SearchableFieldInfo(_message.Message):
    __slots__ = ("source_field_path", "search_record_field", "field_type", "solr_field_name")
    SOURCE_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    SEARCH_RECORD_FIELD_FIELD_NUMBER: _ClassVar[int]
    FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOLR_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    source_field_path: str
    search_record_field: str
    field_type: str
    solr_field_name: str
    def __init__(self, source_field_path: _Optional[str] = ..., search_record_field: _Optional[str] = ..., field_type: _Optional[str] = ..., solr_field_name: _Optional[str] = ...) -> None: ...

class SearchableFieldsResponse(_message.Message):
    __slots__ = ("api_resource_kind", "fields", "total_fields")
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELDS_FIELD_NUMBER: _ClassVar[int]
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    fields: _containers.RepeatedCompositeFieldContainer[SearchableFieldInfo]
    total_fields: int
    def __init__(self, api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., fields: _Optional[_Iterable[_Union[SearchableFieldInfo, _Mapping]]] = ..., total_fields: _Optional[int] = ...) -> None: ...

class ApiResourceSearchQueryInput(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...
