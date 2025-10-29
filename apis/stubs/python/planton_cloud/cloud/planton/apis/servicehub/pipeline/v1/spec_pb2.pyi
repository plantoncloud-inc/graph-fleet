from cloud.planton.apis.connect.githubcredential.v1 import spec_pb2 as _spec_pb2
from cloud.planton.apis.integration.vcs import git_commit_pb2 as _git_commit_pb2
from cloud.planton.apis.integration.vcs import provider_pb2 as _provider_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineSpec(_message.Message):
    __slots__ = ("service_id", "service_slug", "git_commit", "git_repo_provider", "github", "container_image", "is_preview_pipeline")
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_SLUG_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GITHUB_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    IS_PREVIEW_PIPELINE_FIELD_NUMBER: _ClassVar[int]
    service_id: str
    service_slug: str
    git_commit: _git_commit_pb2.GitCommit
    git_repo_provider: _provider_pb2.GitRepoProvider
    github: PipelineGitRepoGithub
    container_image: PipelineContainerImage
    is_preview_pipeline: bool
    def __init__(self, service_id: _Optional[str] = ..., service_slug: _Optional[str] = ..., git_commit: _Optional[_Union[_git_commit_pb2.GitCommit, _Mapping]] = ..., git_repo_provider: _Optional[_Union[_provider_pb2.GitRepoProvider, str]] = ..., github: _Optional[_Union[PipelineGitRepoGithub, _Mapping]] = ..., container_image: _Optional[_Union[PipelineContainerImage, _Mapping]] = ..., is_preview_pipeline: bool = ...) -> None: ...

class PipelineGitRepoGithub(_message.Message):
    __slots__ = ("app_install_info", "repo")
    APP_INSTALL_INFO_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    app_install_info: _spec_pb2.GithubAppInstallInfo
    repo: str
    def __init__(self, app_install_info: _Optional[_Union[_spec_pb2.GithubAppInstallInfo, _Mapping]] = ..., repo: _Optional[str] = ...) -> None: ...

class PipelineContainerImage(_message.Message):
    __slots__ = ("repo", "tag")
    REPO_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    repo: str
    tag: str
    def __init__(self, repo: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...
