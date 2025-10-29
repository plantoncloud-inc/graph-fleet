from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.copilot.copilotchat.chatmessage.v1 import enum_pb2 as _enum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessageSpec(_message.Message):
    __slots__ = ("chat_id", "index", "type", "content", "session_id", "stack_job_id", "user_agent", "api_resource_kind", "api_resource_id", "progress_events")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_EVENTS_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    index: int
    type: _enum_pb2.ChatMessageType
    content: str
    session_id: str
    stack_job_id: str
    user_agent: _enum_pb2.ChatMessageUserAgentType
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    api_resource_id: str
    progress_events: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chat_id: _Optional[str] = ..., index: _Optional[int] = ..., type: _Optional[_Union[_enum_pb2.ChatMessageType, str]] = ..., content: _Optional[str] = ..., session_id: _Optional[str] = ..., stack_job_id: _Optional[str] = ..., user_agent: _Optional[_Union[_enum_pb2.ChatMessageUserAgentType, str]] = ..., api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., api_resource_id: _Optional[str] = ..., progress_events: _Optional[_Iterable[str]] = ...) -> None: ...
