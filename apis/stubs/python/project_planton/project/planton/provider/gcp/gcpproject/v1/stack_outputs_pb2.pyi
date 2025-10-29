from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpProjectStackOutputs(_message.Message):
    __slots__ = ("name", "project_id", "project_number")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    name: str
    project_id: str
    project_number: str
    def __init__(self, name: _Optional[str] = ..., project_id: _Optional[str] = ..., project_number: _Optional[str] = ...) -> None: ...
