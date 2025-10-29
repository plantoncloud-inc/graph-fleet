from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestCredentialResourceSpec(_message.Message):
    __slots__ = ("string_field", "int32_field", "sub_message")
    STRING_FIELD_FIELD_NUMBER: _ClassVar[int]
    INT32_FIELD_FIELD_NUMBER: _ClassVar[int]
    SUB_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    string_field: str
    int32_field: int
    sub_message: TestCredentialResourceSubMessage
    def __init__(self, string_field: _Optional[str] = ..., int32_field: _Optional[int] = ..., sub_message: _Optional[_Union[TestCredentialResourceSubMessage, _Mapping]] = ...) -> None: ...

class TestCredentialResourceSubMessage(_message.Message):
    __slots__ = ("string_field", "int32_field")
    STRING_FIELD_FIELD_NUMBER: _ClassVar[int]
    INT32_FIELD_FIELD_NUMBER: _ClassVar[int]
    string_field: str
    int32_field: int
    def __init__(self, string_field: _Optional[str] = ..., int32_field: _Optional[int] = ...) -> None: ...
