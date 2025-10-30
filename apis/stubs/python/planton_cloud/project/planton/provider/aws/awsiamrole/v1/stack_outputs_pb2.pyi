from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsIamRoleStackOutputs(_message.Message):
    __slots__ = ("role_arn", "role_name")
    ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_arn: str
    role_name: str
    def __init__(self, role_arn: _Optional[str] = ..., role_name: _Optional[str] = ...) -> None: ...
