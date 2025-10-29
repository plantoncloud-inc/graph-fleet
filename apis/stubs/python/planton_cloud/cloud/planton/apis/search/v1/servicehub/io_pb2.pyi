from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchSourceCodeTemplatesInput(_message.Message):
    __slots__ = ("org", "search_text", "page_info", "is_include_official", "is_include_organization_templates", "is_include_github_actions", "is_include_github_workflows", "is_include_cookie_cutter_templates")
    ORG_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_OFFICIAL_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_ORGANIZATION_TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_GITHUB_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_GITHUB_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_COOKIE_CUTTER_TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    org: str
    search_text: str
    page_info: _pagination_pb2.PageInfo
    is_include_official: bool
    is_include_organization_templates: bool
    is_include_github_actions: bool
    is_include_github_workflows: bool
    is_include_cookie_cutter_templates: bool
    def __init__(self, org: _Optional[str] = ..., search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., is_include_official: bool = ..., is_include_organization_templates: bool = ..., is_include_github_actions: bool = ..., is_include_github_workflows: bool = ..., is_include_cookie_cutter_templates: bool = ...) -> None: ...

class VariableEntrySearchRecord(_message.Message):
    __slots__ = ("id", "org", "group_name", "group_id", "name", "value", "value_from", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FROM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    org: str
    group_name: str
    group_id: str
    name: str
    value: str
    value_from: _foreign_key_pb2.ValueFromRef
    description: str
    def __init__(self, id: _Optional[str] = ..., org: _Optional[str] = ..., group_name: _Optional[str] = ..., group_id: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ..., value_from: _Optional[_Union[_foreign_key_pb2.ValueFromRef, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class SecretEntrySearchRecord(_message.Message):
    __slots__ = ("id", "org", "group_name", "group_id", "name", "value", "value_from", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FROM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    org: str
    group_name: str
    group_id: str
    name: str
    value: str
    value_from: _foreign_key_pb2.ValueFromRef
    description: str
    def __init__(self, id: _Optional[str] = ..., org: _Optional[str] = ..., group_name: _Optional[str] = ..., group_id: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ..., value_from: _Optional[_Union[_foreign_key_pb2.ValueFromRef, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class SearchConfigEntriesRequest(_message.Message):
    __slots__ = ("page_info", "org", "search_text")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    org: str
    search_text: str
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., org: _Optional[str] = ..., search_text: _Optional[str] = ...) -> None: ...

class VariableEntrySearchRecordList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[VariableEntrySearchRecord]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[VariableEntrySearchRecord, _Mapping]]] = ...) -> None: ...

class SecretEntrySearchRecordList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[SecretEntrySearchRecord]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[SecretEntrySearchRecord, _Mapping]]] = ...) -> None: ...

class SearchInfraChartsByOrgContextInput(_message.Message):
    __slots__ = ("search_text", "page_info", "org", "is_include_official", "is_include_organization_charts")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_OFFICIAL_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_ORGANIZATION_CHARTS_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    page_info: _pagination_pb2.PageInfo
    org: str
    is_include_official: bool
    is_include_organization_charts: bool
    def __init__(self, search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., org: _Optional[str] = ..., is_include_official: bool = ..., is_include_organization_charts: bool = ...) -> None: ...
