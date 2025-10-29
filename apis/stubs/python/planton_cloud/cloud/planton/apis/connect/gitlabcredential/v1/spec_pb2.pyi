from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GitlabCredentialSpec(_message.Message):
    __slots__ = ("gitlab_connection_host", "group_id", "access_token", "refresh_token")
    GITLAB_CONNECTION_HOST_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    gitlab_connection_host: str
    group_id: str
    access_token: str
    refresh_token: str
    def __init__(self, gitlab_connection_host: _Optional[str] = ..., group_id: _Optional[str] = ..., access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ...) -> None: ...
