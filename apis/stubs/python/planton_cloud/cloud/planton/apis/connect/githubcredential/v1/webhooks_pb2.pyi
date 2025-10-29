from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GithubWebhookPayloadWrapper(_message.Message):
    __slots__ = ("headers", "json_payload")
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    JSON_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    headers: GithubWebhookHeaders
    json_payload: str
    def __init__(self, headers: _Optional[_Union[GithubWebhookHeaders, _Mapping]] = ..., json_payload: _Optional[str] = ...) -> None: ...

class GithubWebhookHeaders(_message.Message):
    __slots__ = ("github_delivery", "hub_signature_256", "user_agent", "github_event", "github_hook_id", "github_hook_installation_target_id", "github_hook_installation_target_type")
    GITHUB_DELIVERY_FIELD_NUMBER: _ClassVar[int]
    HUB_SIGNATURE_256_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    GITHUB_EVENT_FIELD_NUMBER: _ClassVar[int]
    GITHUB_HOOK_ID_FIELD_NUMBER: _ClassVar[int]
    GITHUB_HOOK_INSTALLATION_TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    GITHUB_HOOK_INSTALLATION_TARGET_TYPE_FIELD_NUMBER: _ClassVar[int]
    github_delivery: str
    hub_signature_256: str
    user_agent: str
    github_event: str
    github_hook_id: str
    github_hook_installation_target_id: str
    github_hook_installation_target_type: str
    def __init__(self, github_delivery: _Optional[str] = ..., hub_signature_256: _Optional[str] = ..., user_agent: _Optional[str] = ..., github_event: _Optional[str] = ..., github_hook_id: _Optional[str] = ..., github_hook_installation_target_id: _Optional[str] = ..., github_hook_installation_target_type: _Optional[str] = ...) -> None: ...
