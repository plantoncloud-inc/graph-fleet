from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from cloud.planton.apis.infrahub.infrachart.v1 import param_pb2 as _param_pb2
from cloud.planton.apis.integration.vcs import github_pb2 as _github_pb2
from cloud.planton.apis.integration.vcs import provider_pb2 as _provider_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InfraProjectSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    infra_project_source_unspecified: _ClassVar[InfraProjectSource]
    infra_chart: _ClassVar[InfraProjectSource]
    git_repo: _ClassVar[InfraProjectSource]
infra_project_source_unspecified: InfraProjectSource
infra_chart: InfraProjectSource
git_repo: InfraProjectSource

class InfraProjectSpec(_message.Message):
    __slots__ = ("source", "infra_chart_source", "git_repo_source")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    INFRA_CHART_SOURCE_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: InfraProjectSource
    infra_chart_source: InfraProjectInfraChartSource
    git_repo_source: InfraProjectGitRepoSource
    def __init__(self, source: _Optional[_Union[InfraProjectSource, str]] = ..., infra_chart_source: _Optional[_Union[InfraProjectInfraChartSource, _Mapping]] = ..., git_repo_source: _Optional[_Union[InfraProjectGitRepoSource, _Mapping]] = ...) -> None: ...

class InfraProjectInfraChartSource(_message.Message):
    __slots__ = ("env", "template_yaml", "params")
    ENV_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_YAML_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    env: str
    template_yaml: str
    params: _containers.RepeatedCompositeFieldContainer[_param_pb2.InfraChartParam]
    def __init__(self, env: _Optional[str] = ..., template_yaml: _Optional[str] = ..., params: _Optional[_Iterable[_Union[_param_pb2.InfraChartParam, _Mapping]]] = ...) -> None: ...

class InfraProjectGitRepoSource(_message.Message):
    __slots__ = ("description", "git_repo", "webhook_id", "pipeline_configuration")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_ID_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    description: str
    git_repo: InfraProjectGitRepo
    webhook_id: str
    pipeline_configuration: InfraPipelineConfiguration
    def __init__(self, description: _Optional[str] = ..., git_repo: _Optional[_Union[InfraProjectGitRepo, _Mapping]] = ..., webhook_id: _Optional[str] = ..., pipeline_configuration: _Optional[_Union[InfraPipelineConfiguration, _Mapping]] = ...) -> None: ...

class InfraProjectGitRepo(_message.Message):
    __slots__ = ("owner_name", "name", "default_branch", "browser_url", "clone_url", "git_repo_provider", "github_repo", "project_root")
    OWNER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BRANCH_FIELD_NUMBER: _ClassVar[int]
    BROWSER_URL_FIELD_NUMBER: _ClassVar[int]
    CLONE_URL_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GITHUB_REPO_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ROOT_FIELD_NUMBER: _ClassVar[int]
    owner_name: str
    name: str
    default_branch: str
    browser_url: str
    clone_url: str
    git_repo_provider: _provider_pb2.GitRepoProvider
    github_repo: _github_pb2.GithubRepo
    project_root: str
    def __init__(self, owner_name: _Optional[str] = ..., name: _Optional[str] = ..., default_branch: _Optional[str] = ..., browser_url: _Optional[str] = ..., clone_url: _Optional[str] = ..., git_repo_provider: _Optional[_Union[_provider_pb2.GitRepoProvider, str]] = ..., github_repo: _Optional[_Union[_github_pb2.GithubRepo, _Mapping]] = ..., project_root: _Optional[str] = ...) -> None: ...

class InfraPipelineConfiguration(_message.Message):
    __slots__ = ("disable_pipelines", "disable_deployments", "enable_pull_request_deployments")
    DISABLE_PIPELINES_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PULL_REQUEST_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    disable_pipelines: bool
    disable_deployments: bool
    enable_pull_request_deployments: bool
    def __init__(self, disable_pipelines: bool = ..., disable_deployments: bool = ..., enable_pull_request_deployments: bool = ...) -> None: ...
