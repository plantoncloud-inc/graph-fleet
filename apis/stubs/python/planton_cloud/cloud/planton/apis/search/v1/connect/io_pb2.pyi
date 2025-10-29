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

class GetCredentialsByEnvInput(_message.Message):
    __slots__ = ("org", "env")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...

class ApiResourceSearchRecordsByCredential(_message.Message):
    __slots__ = ("credential_kind", "display_name", "entries")
    CREDENTIAL_KIND_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    credential_kind: _api_resource_kind_pb2.ApiResourceKind
    display_name: str
    entries: _containers.RepeatedCompositeFieldContainer[_record_pb2.ApiResourceSearchRecord]
    def __init__(self, credential_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., display_name: _Optional[str] = ..., entries: _Optional[_Iterable[_Union[_record_pb2.ApiResourceSearchRecord, _Mapping]]] = ...) -> None: ...

class Credentials(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[ApiResourceSearchRecordsByCredential]
    def __init__(self, credentials: _Optional[_Iterable[_Union[ApiResourceSearchRecordsByCredential, _Mapping]]] = ...) -> None: ...

class SearchCredentialApiResourcesByContext(_message.Message):
    __slots__ = ("org", "env", "page_info", "kinds", "search_text")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    KINDS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    page_info: _pagination_pb2.PageInfo
    kinds: _containers.RepeatedScalarFieldContainer[_api_resource_kind_pb2.ApiResourceKind]
    search_text: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., kinds: _Optional[_Iterable[_Union[_api_resource_kind_pb2.ApiResourceKind, str]]] = ..., search_text: _Optional[str] = ...) -> None: ...
