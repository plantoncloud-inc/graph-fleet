from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GithubActionSpec(_message.Message):
    __slots__ = ("selector", "description", "is_official", "is_ready", "git_repo")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_OFFICIAL_FIELD_NUMBER: _ClassVar[int]
    IS_READY_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    description: str
    is_official: bool
    is_ready: bool
    git_repo: GithubActionGitRepo
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., description: _Optional[str] = ..., is_official: bool = ..., is_ready: bool = ..., git_repo: _Optional[_Union[GithubActionGitRepo, _Mapping]] = ...) -> None: ...

class GithubActionGitRepo(_message.Message):
    __slots__ = ("web_url", "overview_markdown_url", "readme_url", "branch", "commit_sha", "repo_path")
    WEB_URL_FIELD_NUMBER: _ClassVar[int]
    OVERVIEW_MARKDOWN_URL_FIELD_NUMBER: _ClassVar[int]
    README_URL_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    REPO_PATH_FIELD_NUMBER: _ClassVar[int]
    web_url: str
    overview_markdown_url: str
    readme_url: str
    branch: str
    commit_sha: str
    repo_path: str
    def __init__(self, web_url: _Optional[str] = ..., overview_markdown_url: _Optional[str] = ..., readme_url: _Optional[str] = ..., branch: _Optional[str] = ..., commit_sha: _Optional[str] = ..., repo_path: _Optional[str] = ...) -> None: ...
