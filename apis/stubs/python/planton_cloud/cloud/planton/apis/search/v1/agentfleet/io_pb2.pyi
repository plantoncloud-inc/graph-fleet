from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.agentfleet.agent.v1 import spec_pb2 as _spec_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchAgentsByOrgContextInput(_message.Message):
    __slots__ = ("search_text", "page_info", "org", "is_include_official", "is_include_org", "frameworks", "runtimes")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_OFFICIAL_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_ORG_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORKS_FIELD_NUMBER: _ClassVar[int]
    RUNTIMES_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    page_info: _pagination_pb2.PageInfo
    org: str
    is_include_official: bool
    is_include_org: bool
    frameworks: _containers.RepeatedScalarFieldContainer[_spec_pb2.AgentFramework]
    runtimes: _containers.RepeatedScalarFieldContainer[_spec_pb2.AgentRuntime]
    def __init__(self, search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., org: _Optional[str] = ..., is_include_official: bool = ..., is_include_org: bool = ..., frameworks: _Optional[_Iterable[_Union[_spec_pb2.AgentFramework, str]]] = ..., runtimes: _Optional[_Iterable[_Union[_spec_pb2.AgentRuntime, str]]] = ...) -> None: ...

class SearchOfficialAgentsInput(_message.Message):
    __slots__ = ("search_text", "page_info", "frameworks", "runtimes")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORKS_FIELD_NUMBER: _ClassVar[int]
    RUNTIMES_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    page_info: _pagination_pb2.PageInfo
    frameworks: _containers.RepeatedScalarFieldContainer[_spec_pb2.AgentFramework]
    runtimes: _containers.RepeatedScalarFieldContainer[_spec_pb2.AgentRuntime]
    def __init__(self, search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., frameworks: _Optional[_Iterable[_Union[_spec_pb2.AgentFramework, str]]] = ..., runtimes: _Optional[_Iterable[_Union[_spec_pb2.AgentRuntime, str]]] = ...) -> None: ...
