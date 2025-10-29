from cloud.planton.apis.agentfleet.execution.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecutionId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class ListExecutionsInput(_message.Message):
    __slots__ = ("page_info", "session_id", "agent_id")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    session_id: str
    agent_id: str
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., session_id: _Optional[str] = ..., agent_id: _Optional[str] = ...) -> None: ...

class ExecutionList(_message.Message):
    __slots__ = ("items", "page_info")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_api_pb2.Execution]
    page_info: _pagination_pb2.PageInfo
    def __init__(self, items: _Optional[_Iterable[_Union[_api_pb2.Execution, _Mapping]]] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ...) -> None: ...
