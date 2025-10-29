from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_FIELD_NUMBER: _ClassVar[int]
default: _descriptor.FieldDescriptor
RECOMMENDED_DEFAULT_FIELD_NUMBER: _ClassVar[int]
recommended_default: _descriptor.FieldDescriptor
RECOMMENDED_DEFAULT_MAP_FIELD_NUMBER: _ClassVar[int]
recommended_default_map: _descriptor.FieldDescriptor
DISPLAY_LABEL_FIELD_NUMBER: _ClassVar[int]
display_label: _descriptor.FieldDescriptor

class KeyValuePair(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
