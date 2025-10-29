from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from cloud.planton.apis.connect.githubcredential.v1 import spec_pb2 as _spec_pb2
from cloud.planton.apis.integration.vcs import git_commit_pb2 as _git_commit_pb2
from cloud.planton.apis.integration.vcs import provider_pb2 as _provider_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InfraPipelineSpec(_message.Message):
    __slots__ = ("infra_project_id", "infra_project_slug", "git_commit", "git_repo_provider", "github", "is_preview_pipeline")
    INFRA_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    INFRA_PROJECT_SLUG_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GITHUB_FIELD_NUMBER: _ClassVar[int]
    IS_PREVIEW_PIPELINE_FIELD_NUMBER: _ClassVar[int]
    infra_project_id: str
    infra_project_slug: str
    git_commit: _git_commit_pb2.GitCommit
    git_repo_provider: _provider_pb2.GitRepoProvider
    github: InfraPipelineGitRepoGithub
    is_preview_pipeline: bool
    def __init__(self, infra_project_id: _Optional[str] = ..., infra_project_slug: _Optional[str] = ..., git_commit: _Optional[_Union[_git_commit_pb2.GitCommit, _Mapping]] = ..., git_repo_provider: _Optional[_Union[_provider_pb2.GitRepoProvider, str]] = ..., github: _Optional[_Union[InfraPipelineGitRepoGithub, _Mapping]] = ..., is_preview_pipeline: bool = ...) -> None: ...

class InfraPipelineGitRepoGithub(_message.Message):
    __slots__ = ("app_install_info", "repo")
    APP_INSTALL_INFO_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    app_install_info: _spec_pb2.GithubAppInstallInfo
    repo: str
    def __init__(self, app_install_info: _Optional[_Union[_spec_pb2.GithubAppInstallInfo, _Mapping]] = ..., repo: _Optional[str] = ...) -> None: ...
