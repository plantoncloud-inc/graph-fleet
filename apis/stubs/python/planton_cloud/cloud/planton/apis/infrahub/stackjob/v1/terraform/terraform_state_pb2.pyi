from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TerraformStateJson(_message.Message):
    __slots__ = ("format_version", "terraform_version", "values")
    FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    TERRAFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    format_version: str
    terraform_version: str
    values: TerraformStateJsonValues
    def __init__(self, format_version: _Optional[str] = ..., terraform_version: _Optional[str] = ..., values: _Optional[_Union[TerraformStateJsonValues, _Mapping]] = ...) -> None: ...

class TerraformStateJsonValues(_message.Message):
    __slots__ = ("outputs", "root_module")
    class OutputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TerraformStateJsonOutputValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[TerraformStateJsonOutputValue, _Mapping]] = ...) -> None: ...
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    ROOT_MODULE_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.MessageMap[str, TerraformStateJsonOutputValue]
    root_module: TerraformStateJsonRootModule
    def __init__(self, outputs: _Optional[_Mapping[str, TerraformStateJsonOutputValue]] = ..., root_module: _Optional[_Union[TerraformStateJsonRootModule, _Mapping]] = ...) -> None: ...

class TerraformStateJsonOutputValue(_message.Message):
    __slots__ = ("sensitive", "value", "type")
    SENSITIVE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    sensitive: bool
    value: _struct_pb2.Value
    type: _struct_pb2.Value
    def __init__(self, sensitive: bool = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., type: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class TerraformStateJsonRootModule(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[TerraformStateJsonResource]
    def __init__(self, resources: _Optional[_Iterable[_Union[TerraformStateJsonResource, _Mapping]]] = ...) -> None: ...

class TerraformStateJsonResource(_message.Message):
    __slots__ = ("address", "mode", "type", "name", "index", "provider_name", "schema_version", "values", "sensitive_values", "depends_on")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    SENSITIVE_VALUES_FIELD_NUMBER: _ClassVar[int]
    DEPENDS_ON_FIELD_NUMBER: _ClassVar[int]
    address: str
    mode: str
    type: str
    name: str
    index: str
    provider_name: str
    schema_version: int
    values: _struct_pb2.Struct
    sensitive_values: _struct_pb2.Struct
    depends_on: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, address: _Optional[str] = ..., mode: _Optional[str] = ..., type: _Optional[str] = ..., name: _Optional[str] = ..., index: _Optional[str] = ..., provider_name: _Optional[str] = ..., schema_version: _Optional[int] = ..., values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., sensitive_values: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., depends_on: _Optional[_Iterable[str]] = ...) -> None: ...
