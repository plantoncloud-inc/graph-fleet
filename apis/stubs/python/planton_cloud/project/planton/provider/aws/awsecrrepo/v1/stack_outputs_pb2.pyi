from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEcrRepoStackOutputs(_message.Message):
    __slots__ = ("repository_name", "repository_url", "repository_arn", "registry_id")
    REPOSITORY_NAME_FIELD_NUMBER: _ClassVar[int]
    REPOSITORY_URL_FIELD_NUMBER: _ClassVar[int]
    REPOSITORY_ARN_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_ID_FIELD_NUMBER: _ClassVar[int]
    repository_name: str
    repository_url: str
    repository_arn: str
    registry_id: str
    def __init__(self, repository_name: _Optional[str] = ..., repository_url: _Optional[str] = ..., repository_arn: _Optional[str] = ..., registry_id: _Optional[str] = ...) -> None: ...
