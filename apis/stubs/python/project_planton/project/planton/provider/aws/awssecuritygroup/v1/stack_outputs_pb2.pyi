from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsSecurityGroupStackOutputs(_message.Message):
    __slots__ = ("security_group_id",)
    SECURITY_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    security_group_id: str
    def __init__(self, security_group_id: _Optional[str] = ...) -> None: ...
