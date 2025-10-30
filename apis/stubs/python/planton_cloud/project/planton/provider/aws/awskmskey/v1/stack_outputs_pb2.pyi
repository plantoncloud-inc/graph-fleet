from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsKmsKeyStackOutputs(_message.Message):
    __slots__ = ("key_id", "key_arn", "alias_name", "rotation_enabled")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ARN_FIELD_NUMBER: _ClassVar[int]
    ALIAS_NAME_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    key_arn: str
    alias_name: str
    rotation_enabled: bool
    def __init__(self, key_id: _Optional[str] = ..., key_arn: _Optional[str] = ..., alias_name: _Optional[str] = ..., rotation_enabled: bool = ...) -> None: ...
