from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComputedFieldsTest(_message.Message):
    __slots__ = ("required_string_field", "computed_string_field")
    REQUIRED_STRING_FIELD_FIELD_NUMBER: _ClassVar[int]
    COMPUTED_STRING_FIELD_FIELD_NUMBER: _ClassVar[int]
    required_string_field: str
    computed_string_field: str
    def __init__(self, required_string_field: _Optional[str] = ..., computed_string_field: _Optional[str] = ...) -> None: ...

class NestedComputedFieldsTest(_message.Message):
    __slots__ = ("nested_computed_field",)
    NESTED_COMPUTED_FIELD_FIELD_NUMBER: _ClassVar[int]
    nested_computed_field: ComputedFieldsTest
    def __init__(self, nested_computed_field: _Optional[_Union[ComputedFieldsTest, _Mapping]] = ...) -> None: ...

class RepeatedComputedFieldsTest(_message.Message):
    __slots__ = ("repeated_computed_field",)
    REPEATED_COMPUTED_FIELD_FIELD_NUMBER: _ClassVar[int]
    repeated_computed_field: _containers.RepeatedCompositeFieldContainer[ComputedFieldsTest]
    def __init__(self, repeated_computed_field: _Optional[_Iterable[_Union[ComputedFieldsTest, _Mapping]]] = ...) -> None: ...
