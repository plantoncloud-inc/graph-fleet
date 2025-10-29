from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GitAuthSecretArgs(_message.Message):
    __slots__ = ("git_host_base_url", "git_username", "git_token")
    GIT_HOST_BASE_URL_FIELD_NUMBER: _ClassVar[int]
    GIT_USERNAME_FIELD_NUMBER: _ClassVar[int]
    GIT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    git_host_base_url: str
    git_username: str
    git_token: str
    def __init__(self, git_host_base_url: _Optional[str] = ..., git_username: _Optional[str] = ..., git_token: _Optional[str] = ...) -> None: ...
