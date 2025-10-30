from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsProviderConfig(_message.Message):
    __slots__ = ("account_id", "access_key_id", "secret_access_key", "region", "session_token")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    access_key_id: str
    secret_access_key: str
    region: str
    session_token: str
    def __init__(self, account_id: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ..., region: _Optional[str] = ..., session_token: _Optional[str] = ...) -> None: ...
