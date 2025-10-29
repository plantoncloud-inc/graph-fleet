from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class MessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    message_type_unspecified: _ClassVar[MessageType]
    human: _ClassVar[MessageType]
    ai: _ClassVar[MessageType]
    tool: _ClassVar[MessageType]
    system: _ClassVar[MessageType]

class ToolCallStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    tool_call_status_unspecified: _ClassVar[ToolCallStatus]
    tool_call_status_pending: _ClassVar[ToolCallStatus]
    tool_call_status_completed: _ClassVar[ToolCallStatus]
    tool_call_status_error: _ClassVar[ToolCallStatus]

class TodoStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    todo_status_unspecified: _ClassVar[TodoStatus]
    todo_status_pending: _ClassVar[TodoStatus]
    todo_status_in_progress: _ClassVar[TodoStatus]
    todo_status_completed: _ClassVar[TodoStatus]
    todo_status_cancelled: _ClassVar[TodoStatus]
message_type_unspecified: MessageType
human: MessageType
ai: MessageType
tool: MessageType
system: MessageType
tool_call_status_unspecified: ToolCallStatus
tool_call_status_pending: ToolCallStatus
tool_call_status_completed: ToolCallStatus
tool_call_status_error: ToolCallStatus
todo_status_unspecified: TodoStatus
todo_status_pending: TodoStatus
todo_status_in_progress: TodoStatus
todo_status_completed: TodoStatus
todo_status_cancelled: TodoStatus
