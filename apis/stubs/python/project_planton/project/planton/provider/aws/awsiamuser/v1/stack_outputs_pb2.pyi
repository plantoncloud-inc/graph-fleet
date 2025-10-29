from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsIamUserStackOutputs(_message.Message):
    __slots__ = ("user_arn", "access_key_id", "secret_access_key", "console_url", "user_name", "user_id")
    USER_ARN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    CONSOLE_URL_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_arn: str
    access_key_id: str
    secret_access_key: str
    console_url: str
    user_name: str
    user_id: str
    def __init__(self, user_arn: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ..., console_url: _Optional[str] = ..., user_name: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...
