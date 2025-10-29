from cloud.planton.apis.connect.githubcredential.v1 import webhooks_pb2 as _webhooks_pb2
from cloud.planton.apis.connect.gitlabcredential.v1 import webhooks_pb2 as _webhooks_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VcsWebhookWrapper(_message.Message):
    __slots__ = ("hook_id", "github", "gitlab")
    HOOK_ID_FIELD_NUMBER: _ClassVar[int]
    GITHUB_FIELD_NUMBER: _ClassVar[int]
    GITLAB_FIELD_NUMBER: _ClassVar[int]
    hook_id: str
    github: _webhooks_pb2.GithubWebhookPayloadWrapper
    gitlab: _webhooks_pb2_1.GitlabWebhookPayloadWrapper
    def __init__(self, hook_id: _Optional[str] = ..., github: _Optional[_Union[_webhooks_pb2.GithubWebhookPayloadWrapper, _Mapping]] = ..., gitlab: _Optional[_Union[_webhooks_pb2_1.GitlabWebhookPayloadWrapper, _Mapping]] = ...) -> None: ...
