from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    chat_mode_unspecified: _ClassVar[ChatMode]
    ops: _ClassVar[ChatMode]
    dev: _ClassVar[ChatMode]
chat_mode_unspecified: ChatMode
ops: ChatMode
dev: ChatMode
