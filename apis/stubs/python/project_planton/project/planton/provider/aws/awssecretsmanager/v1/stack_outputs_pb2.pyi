from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsSecretsManagerStackOutputs(_message.Message):
    __slots__ = ("secret_arn_map",)
    class SecretArnMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SECRET_ARN_MAP_FIELD_NUMBER: _ClassVar[int]
    secret_arn_map: _containers.ScalarMap[str, str]
    def __init__(self, secret_arn_map: _Optional[_Mapping[str, str]] = ...) -> None: ...
