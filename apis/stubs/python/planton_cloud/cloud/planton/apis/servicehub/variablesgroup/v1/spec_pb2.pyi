from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VariablesGroupSpec(_message.Message):
    __slots__ = ("description", "entries")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    description: str
    entries: _containers.RepeatedCompositeFieldContainer[VariablesGroupEntry]
    def __init__(self, description: _Optional[str] = ..., entries: _Optional[_Iterable[_Union[VariablesGroupEntry, _Mapping]]] = ...) -> None: ...

class VariablesGroupEntry(_message.Message):
    __slots__ = ("name", "description", "value", "value_from")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FROM_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    value: str
    value_from: _foreign_key_pb2.ValueFromRef
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., value: _Optional[str] = ..., value_from: _Optional[_Union[_foreign_key_pb2.ValueFromRef, _Mapping]] = ...) -> None: ...
