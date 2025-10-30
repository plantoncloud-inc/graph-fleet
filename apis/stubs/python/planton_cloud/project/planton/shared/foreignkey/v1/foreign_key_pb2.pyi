from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_KIND_FIELD_NUMBER: _ClassVar[int]
default_kind: _descriptor.FieldDescriptor
DEFAULT_KIND_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
default_kind_field_path: _descriptor.FieldDescriptor

class ValueFromRef(_message.Message):
    __slots__ = ("kind", "env", "name", "field_path")
    KIND_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    kind: _cloud_resource_kind_pb2.CloudResourceKind
    env: str
    name: str
    field_path: str
    def __init__(self, kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., env: _Optional[str] = ..., name: _Optional[str] = ..., field_path: _Optional[str] = ...) -> None: ...

class StringValueOrRef(_message.Message):
    __slots__ = ("value", "value_from")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FROM_FIELD_NUMBER: _ClassVar[int]
    value: str
    value_from: ValueFromRef
    def __init__(self, value: _Optional[str] = ..., value_from: _Optional[_Union[ValueFromRef, _Mapping]] = ...) -> None: ...

class Int32ValueOrRef(_message.Message):
    __slots__ = ("value", "value_from")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FROM_FIELD_NUMBER: _ClassVar[int]
    value: int
    value_from: ValueFromRef
    def __init__(self, value: _Optional[int] = ..., value_from: _Optional[_Union[ValueFromRef, _Mapping]] = ...) -> None: ...
