from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParamType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    param_type_unspecified: _ClassVar[ParamType]
    string: _ClassVar[ParamType]
    number: _ClassVar[ParamType]
    bool: _ClassVar[ParamType]
    list: _ClassVar[ParamType]
param_type_unspecified: ParamType
string: ParamType
number: ParamType
bool: ParamType
list: ParamType

class InfraChartParam(_message.Message):
    __slots__ = ("name", "description", "type", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    type: ParamType
    value: _struct_pb2.Value
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., type: _Optional[_Union[ParamType, str]] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class InfraChartParams(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _containers.RepeatedCompositeFieldContainer[InfraChartParam]
    def __init__(self, params: _Optional[_Iterable[_Union[InfraChartParam, _Mapping]]] = ...) -> None: ...
