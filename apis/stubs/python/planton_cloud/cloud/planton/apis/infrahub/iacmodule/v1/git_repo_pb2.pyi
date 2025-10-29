from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IacModuleGitRepo(_message.Message):
    __slots__ = ("clone_url", "git_credential_id", "web_url", "overview_markdown_url", "readme_url", "branch", "commit_sha", "project_dir", "repo_path")
    CLONE_URL_FIELD_NUMBER: _ClassVar[int]
    GIT_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    WEB_URL_FIELD_NUMBER: _ClassVar[int]
    OVERVIEW_MARKDOWN_URL_FIELD_NUMBER: _ClassVar[int]
    README_URL_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    PROJECT_DIR_FIELD_NUMBER: _ClassVar[int]
    REPO_PATH_FIELD_NUMBER: _ClassVar[int]
    clone_url: str
    git_credential_id: str
    web_url: str
    overview_markdown_url: str
    readme_url: str
    branch: str
    commit_sha: str
    project_dir: str
    repo_path: str
    def __init__(self, clone_url: _Optional[str] = ..., git_credential_id: _Optional[str] = ..., web_url: _Optional[str] = ..., overview_markdown_url: _Optional[str] = ..., readme_url: _Optional[str] = ..., branch: _Optional[str] = ..., commit_sha: _Optional[str] = ..., project_dir: _Optional[str] = ..., repo_path: _Optional[str] = ...) -> None: ...

class IacGitRepo(_message.Message):
    __slots__ = ("clone_url", "branch", "commit_sha", "project_dir", "auth")
    CLONE_URL_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    PROJECT_DIR_FIELD_NUMBER: _ClassVar[int]
    AUTH_FIELD_NUMBER: _ClassVar[int]
    clone_url: str
    branch: str
    commit_sha: str
    project_dir: str
    auth: IacGitRepoAuth
    def __init__(self, clone_url: _Optional[str] = ..., branch: _Optional[str] = ..., commit_sha: _Optional[str] = ..., project_dir: _Optional[str] = ..., auth: _Optional[_Union[IacGitRepoAuth, _Mapping]] = ...) -> None: ...

class IacGitRepoAuth(_message.Message):
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
