from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GitCredentialSpec(_message.Message):
    __slots__ = ("username", "password", "ssh_private_key", "personal_access_token")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SSH_PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    ssh_private_key: str
    personal_access_token: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., ssh_private_key: _Optional[str] = ..., personal_access_token: _Optional[str] = ...) -> None: ...
