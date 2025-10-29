from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GithubRepo(_message.Message):
    __slots__ = ("github_credential_id", "organization")
    GITHUB_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    github_credential_id: str
    organization: str
    def __init__(self, github_credential_id: _Optional[str] = ..., organization: _Optional[str] = ...) -> None: ...
