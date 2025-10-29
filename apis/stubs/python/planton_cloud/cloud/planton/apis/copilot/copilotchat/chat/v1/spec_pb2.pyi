from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.copilot.copilotchat.chat.v1 import enum_pb2 as _enum_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatSpec(_message.Message):
    __slots__ = ("api_resource_kind", "api_resource_id", "is_shared", "chat_mode")
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_SHARED_FIELD_NUMBER: _ClassVar[int]
    CHAT_MODE_FIELD_NUMBER: _ClassVar[int]
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    api_resource_id: str
    is_shared: bool
    chat_mode: _enum_pb2.ChatMode
    def __init__(self, api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., api_resource_id: _Optional[str] = ..., is_shared: bool = ..., chat_mode: _Optional[_Union[_enum_pb2.ChatMode, str]] = ...) -> None: ...
