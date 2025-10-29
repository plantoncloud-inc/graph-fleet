from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TektonTaskLogEntry(_message.Message):
    __slots__ = ("owner", "task_name", "log_message")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TASK_NAME_FIELD_NUMBER: _ClassVar[int]
    LOG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    owner: str
    task_name: str
    log_message: str
    def __init__(self, owner: _Optional[str] = ..., task_name: _Optional[str] = ..., log_message: _Optional[str] = ...) -> None: ...
