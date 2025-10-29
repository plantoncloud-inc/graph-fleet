from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class EnglishAcronym(_message.Message):
    __slots__ = ()
    class EnglishAcronymEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        unspecified: _ClassVar[EnglishAcronym.EnglishAcronymEnum]
        NW: _ClassVar[EnglishAcronym.EnglishAcronymEnum]
        RPC: _ClassVar[EnglishAcronym.EnglishAcronymEnum]
    unspecified: EnglishAcronym.EnglishAcronymEnum
    NW: EnglishAcronym.EnglishAcronymEnum
    RPC: EnglishAcronym.EnglishAcronymEnum
    def __init__(self) -> None: ...
