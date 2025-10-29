from cloud.planton.apis.agentfleet.session.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListSessionsInput(_message.Message):
    __slots__ = ("page_info", "agent_id")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    agent_id: str
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., agent_id: _Optional[str] = ...) -> None: ...

class SessionList(_message.Message):
    __slots__ = ("items", "page_info")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_api_pb2.Session]
    page_info: _pagination_pb2.PageInfo
    def __init__(self, items: _Optional[_Iterable[_Union[_api_pb2.Session, _Mapping]]] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ...) -> None: ...
