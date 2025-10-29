from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsLambdaStackOutputs(_message.Message):
    __slots__ = ("function_arn", "function_name", "log_group_name", "role_arn", "layer_arns")
    FUNCTION_ARN_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    LOG_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    LAYER_ARNS_FIELD_NUMBER: _ClassVar[int]
    function_arn: str
    function_name: str
    log_group_name: str
    role_arn: str
    layer_arns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, function_arn: _Optional[str] = ..., function_name: _Optional[str] = ..., log_group_name: _Optional[str] = ..., role_arn: _Optional[str] = ..., layer_arns: _Optional[_Iterable[str]] = ...) -> None: ...
