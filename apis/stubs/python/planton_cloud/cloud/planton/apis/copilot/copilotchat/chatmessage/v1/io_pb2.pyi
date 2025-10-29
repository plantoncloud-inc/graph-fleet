from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.copilot.copilotchat.chatmessage.v1 import api_pb2 as _api_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessageId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class SendMessageInput(_message.Message):
    __slots__ = ("chat_id", "content")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    content: str
    def __init__(self, chat_id: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class ChatMessages(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.ChatMessage]
    def __init__(self, entries: _Optional[_Iterable[_Union[_api_pb2.ChatMessage, _Mapping]]] = ...) -> None: ...

class ChatSessionId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class GetChatMessageStreamInput(_message.Message):
    __slots__ = ("chat_id", "session_id")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    session_id: str
    def __init__(self, chat_id: _Optional[str] = ..., session_id: _Optional[str] = ...) -> None: ...

class ChatMessagesCountCurrentAndPreviousMonthInput(_message.Message):
    __slots__ = ("org",)
    ORG_FIELD_NUMBER: _ClassVar[int]
    org: str
    def __init__(self, org: _Optional[str] = ...) -> None: ...

class ChatMessagesCountCurrentAndPreviousMonth(_message.Message):
    __slots__ = ("current_month_count", "previous_month_count")
    CURRENT_MONTH_COUNT_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_MONTH_COUNT_FIELD_NUMBER: _ClassVar[int]
    current_month_count: float
    previous_month_count: float
    def __init__(self, current_month_count: _Optional[float] = ..., previous_month_count: _Optional[float] = ...) -> None: ...
