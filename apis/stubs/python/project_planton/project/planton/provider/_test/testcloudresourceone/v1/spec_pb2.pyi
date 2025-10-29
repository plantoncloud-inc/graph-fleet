from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestCloudResourceOneSpec(_message.Message):
    __slots__ = ("string_field", "string_no_default", "int32_field", "int64_field", "uint32_field", "uint64_field", "float_field", "double_field", "bool_field", "nested")
    STRING_FIELD_FIELD_NUMBER: _ClassVar[int]
    STRING_NO_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    INT32_FIELD_FIELD_NUMBER: _ClassVar[int]
    INT64_FIELD_FIELD_NUMBER: _ClassVar[int]
    UINT32_FIELD_FIELD_NUMBER: _ClassVar[int]
    UINT64_FIELD_FIELD_NUMBER: _ClassVar[int]
    FLOAT_FIELD_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_FIELD_NUMBER: _ClassVar[int]
    NESTED_FIELD_NUMBER: _ClassVar[int]
    string_field: str
    string_no_default: str
    int32_field: int
    int64_field: int
    uint32_field: int
    uint64_field: int
    float_field: float
    double_field: float
    bool_field: bool
    nested: TestNestedMessage
    def __init__(self, string_field: _Optional[str] = ..., string_no_default: _Optional[str] = ..., int32_field: _Optional[int] = ..., int64_field: _Optional[int] = ..., uint32_field: _Optional[int] = ..., uint64_field: _Optional[int] = ..., float_field: _Optional[float] = ..., double_field: _Optional[float] = ..., bool_field: bool = ..., nested: _Optional[_Union[TestNestedMessage, _Mapping]] = ...) -> None: ...

class TestNestedMessage(_message.Message):
    __slots__ = ("nested_string", "nested_int")
    NESTED_STRING_FIELD_NUMBER: _ClassVar[int]
    NESTED_INT_FIELD_NUMBER: _ClassVar[int]
    nested_string: str
    nested_int: int
    def __init__(self, nested_string: _Optional[str] = ..., nested_int: _Optional[int] = ...) -> None: ...
