from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GitCommit(_message.Message):
    __slots__ = ("webhook_id", "hook_delivery_id", "repo", "author", "branch", "sha", "message", "is_pull_request_commit", "pull_request_title", "author_email", "author_avatar_url", "commit_url", "pull_request_url", "pull_request_number", "touched_files", "pull_request_target_branch")
    WEBHOOK_ID_FIELD_NUMBER: _ClassVar[int]
    HOOK_DELIVERY_ID_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    SHA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IS_PULL_REQUEST_COMMIT_FIELD_NUMBER: _ClassVar[int]
    PULL_REQUEST_TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_EMAIL_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    COMMIT_URL_FIELD_NUMBER: _ClassVar[int]
    PULL_REQUEST_URL_FIELD_NUMBER: _ClassVar[int]
    PULL_REQUEST_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TOUCHED_FILES_FIELD_NUMBER: _ClassVar[int]
    PULL_REQUEST_TARGET_BRANCH_FIELD_NUMBER: _ClassVar[int]
    webhook_id: str
    hook_delivery_id: str
    repo: str
    author: str
    branch: str
    sha: str
    message: str
    is_pull_request_commit: bool
    pull_request_title: str
    author_email: str
    author_avatar_url: str
    commit_url: str
    pull_request_url: str
    pull_request_number: int
    touched_files: _containers.RepeatedScalarFieldContainer[str]
    pull_request_target_branch: str
    def __init__(self, webhook_id: _Optional[str] = ..., hook_delivery_id: _Optional[str] = ..., repo: _Optional[str] = ..., author: _Optional[str] = ..., branch: _Optional[str] = ..., sha: _Optional[str] = ..., message: _Optional[str] = ..., is_pull_request_commit: bool = ..., pull_request_title: _Optional[str] = ..., author_email: _Optional[str] = ..., author_avatar_url: _Optional[str] = ..., commit_url: _Optional[str] = ..., pull_request_url: _Optional[str] = ..., pull_request_number: _Optional[int] = ..., touched_files: _Optional[_Iterable[str]] = ..., pull_request_target_branch: _Optional[str] = ...) -> None: ...
