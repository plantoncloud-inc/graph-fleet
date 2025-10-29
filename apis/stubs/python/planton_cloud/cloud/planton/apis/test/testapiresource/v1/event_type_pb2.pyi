from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TestApiResourceApiResourceEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    unspecified: _ClassVar[TestApiResourceApiResourceEventType]
    created: _ClassVar[TestApiResourceApiResourceEventType]
    updated: _ClassVar[TestApiResourceApiResourceEventType]
    deleted: _ClassVar[TestApiResourceApiResourceEventType]
    restored: _ClassVar[TestApiResourceApiResourceEventType]
unspecified: TestApiResourceApiResourceEventType
created: TestApiResourceApiResourceEventType
updated: TestApiResourceApiResourceEventType
deleted: TestApiResourceApiResourceEventType
restored: TestApiResourceApiResourceEventType
