from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.copilot.copilotchat.chat.v1 import api_pb2 as _api_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class ChatList(_message.Message):
    __slots__ = ("total_pages", "today", "yesterday", "previous")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    TODAY_FIELD_NUMBER: _ClassVar[int]
    YESTERDAY_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    today: _containers.RepeatedCompositeFieldContainer[_api_pb2.Chat]
    yesterday: _containers.RepeatedCompositeFieldContainer[_api_pb2.Chat]
    previous: _containers.RepeatedCompositeFieldContainer[_api_pb2.Chat]
    def __init__(self, total_pages: _Optional[int] = ..., today: _Optional[_Iterable[_Union[_api_pb2.Chat, _Mapping]]] = ..., yesterday: _Optional[_Iterable[_Union[_api_pb2.Chat, _Mapping]]] = ..., previous: _Optional[_Iterable[_Union[_api_pb2.Chat, _Mapping]]] = ...) -> None: ...

class GetApiResourceChatInput(_message.Message):
    __slots__ = ("api_resource_kind", "api_resource_id")
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    api_resource_id: str
    def __init__(self, api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., api_resource_id: _Optional[str] = ...) -> None: ...
