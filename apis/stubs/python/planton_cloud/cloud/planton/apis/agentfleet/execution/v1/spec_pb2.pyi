from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.agentfleet.execution.v1 import enum_pb2 as _enum_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecutionSpec(_message.Message):
    __slots__ = ("session_id", "agent_id", "message", "execution_config")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    agent_id: str
    message: str
    execution_config: ExecutionConfig
    def __init__(self, session_id: _Optional[str] = ..., agent_id: _Optional[str] = ..., message: _Optional[str] = ..., execution_config: _Optional[_Union[ExecutionConfig, _Mapping]] = ...) -> None: ...

class ExecutionConfig(_message.Message):
    __slots__ = ("model_name",)
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    def __init__(self, model_name: _Optional[str] = ...) -> None: ...

class AgentMessage(_message.Message):
    __slots__ = ("type", "content", "timestamp", "tool_calls")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    type: _enum_pb2.MessageType
    content: str
    timestamp: str
    tool_calls: _containers.RepeatedCompositeFieldContainer[ToolCall]
    def __init__(self, type: _Optional[_Union[_enum_pb2.MessageType, str]] = ..., content: _Optional[str] = ..., timestamp: _Optional[str] = ..., tool_calls: _Optional[_Iterable[_Union[ToolCall, _Mapping]]] = ...) -> None: ...

class ToolCall(_message.Message):
    __slots__ = ("id", "name", "args", "result", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    args: _struct_pb2.Struct
    result: str
    status: _enum_pb2.ToolCallStatus
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., args: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., result: _Optional[str] = ..., status: _Optional[_Union[_enum_pb2.ToolCallStatus, str]] = ...) -> None: ...
