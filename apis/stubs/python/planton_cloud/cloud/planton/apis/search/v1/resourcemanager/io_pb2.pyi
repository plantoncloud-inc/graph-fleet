from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetContextHierarchyInput(_message.Message):
    __slots__ = ("search_text",)
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    def __init__(self, search_text: _Optional[str] = ...) -> None: ...

class ContextOrg(_message.Message):
    __slots__ = ("org_id", "org_name", "org_slug", "envs")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_NAME_FIELD_NUMBER: _ClassVar[int]
    ORG_SLUG_FIELD_NUMBER: _ClassVar[int]
    ENVS_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    org_name: str
    org_slug: str
    envs: _containers.RepeatedCompositeFieldContainer[ContextEnv]
    def __init__(self, org_id: _Optional[str] = ..., org_name: _Optional[str] = ..., org_slug: _Optional[str] = ..., envs: _Optional[_Iterable[_Union[ContextEnv, _Mapping]]] = ...) -> None: ...

class ContextEnv(_message.Message):
    __slots__ = ("env_id", "env_name", "env_slug")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    ENV_NAME_FIELD_NUMBER: _ClassVar[int]
    ENV_SLUG_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    env_name: str
    env_slug: str
    def __init__(self, env_id: _Optional[str] = ..., env_name: _Optional[str] = ..., env_slug: _Optional[str] = ...) -> None: ...

class OrganizationContextHierarchy(_message.Message):
    __slots__ = ("orgs",)
    ORGS_FIELD_NUMBER: _ClassVar[int]
    orgs: _containers.RepeatedCompositeFieldContainer[ContextOrg]
    def __init__(self, orgs: _Optional[_Iterable[_Union[ContextOrg, _Mapping]]] = ...) -> None: ...

class SearchQuickActionsRequest(_message.Message):
    __slots__ = ("page_info", "search_text")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    search_text: str
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., search_text: _Optional[str] = ...) -> None: ...
