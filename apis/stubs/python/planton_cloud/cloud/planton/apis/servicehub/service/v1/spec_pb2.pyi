from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from cloud.planton.apis.integration.vcs import github_pb2 as _github_pb2
from cloud.planton.apis.integration.vcs import provider_pb2 as _provider_pb2
from cloud.planton.apis.servicehub.service.v1 import enum_pb2 as _enum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceSpec(_message.Message):
    __slots__ = ("description", "git_repo", "webhook_id", "pipeline_configuration", "ingress", "deployment_environments")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_ID_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    description: str
    git_repo: ServiceGitRepo
    webhook_id: str
    pipeline_configuration: ServicePipelineConfiguration
    ingress: ServiceIngressConfiguration
    deployment_environments: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, description: _Optional[str] = ..., git_repo: _Optional[_Union[ServiceGitRepo, _Mapping]] = ..., webhook_id: _Optional[str] = ..., pipeline_configuration: _Optional[_Union[ServicePipelineConfiguration, _Mapping]] = ..., ingress: _Optional[_Union[ServiceIngressConfiguration, _Mapping]] = ..., deployment_environments: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceGitRepo(_message.Message):
    __slots__ = ("owner_name", "name", "default_branch", "browser_url", "clone_url", "git_repo_provider", "github_repo", "project_root", "trigger_paths", "sparse_checkout_directories")
    OWNER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BRANCH_FIELD_NUMBER: _ClassVar[int]
    BROWSER_URL_FIELD_NUMBER: _ClassVar[int]
    CLONE_URL_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GITHUB_REPO_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ROOT_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PATHS_FIELD_NUMBER: _ClassVar[int]
    SPARSE_CHECKOUT_DIRECTORIES_FIELD_NUMBER: _ClassVar[int]
    owner_name: str
    name: str
    default_branch: str
    browser_url: str
    clone_url: str
    git_repo_provider: _provider_pb2.GitRepoProvider
    github_repo: _github_pb2.GithubRepo
    project_root: str
    trigger_paths: _containers.RepeatedScalarFieldContainer[str]
    sparse_checkout_directories: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, owner_name: _Optional[str] = ..., name: _Optional[str] = ..., default_branch: _Optional[str] = ..., browser_url: _Optional[str] = ..., clone_url: _Optional[str] = ..., git_repo_provider: _Optional[_Union[_provider_pb2.GitRepoProvider, str]] = ..., github_repo: _Optional[_Union[_github_pb2.GithubRepo, _Mapping]] = ..., project_root: _Optional[str] = ..., trigger_paths: _Optional[_Iterable[str]] = ..., sparse_checkout_directories: _Optional[_Iterable[str]] = ...) -> None: ...

class ServicePipelineConfiguration(_message.Message):
    __slots__ = ("pipeline_provider", "tekton_pipeline_yaml_directory", "image_build_method", "disable_pipelines", "disable_deployments", "enable_pull_request_deployments", "image_repository_path", "params", "pipeline_branch", "enable_pull_request_builds")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PIPELINE_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TEKTON_PIPELINE_YAML_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BUILD_METHOD_FIELD_NUMBER: _ClassVar[int]
    DISABLE_PIPELINES_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PULL_REQUEST_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_REPOSITORY_PATH_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_BRANCH_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PULL_REQUEST_BUILDS_FIELD_NUMBER: _ClassVar[int]
    pipeline_provider: _enum_pb2.PipelineProvider
    tekton_pipeline_yaml_directory: str
    image_build_method: _enum_pb2.ImageBuildMethod
    disable_pipelines: bool
    disable_deployments: bool
    enable_pull_request_deployments: bool
    image_repository_path: str
    params: _containers.ScalarMap[str, str]
    pipeline_branch: str
    enable_pull_request_builds: bool
    def __init__(self, pipeline_provider: _Optional[_Union[_enum_pb2.PipelineProvider, str]] = ..., tekton_pipeline_yaml_directory: _Optional[str] = ..., image_build_method: _Optional[_Union[_enum_pb2.ImageBuildMethod, str]] = ..., disable_pipelines: bool = ..., disable_deployments: bool = ..., enable_pull_request_deployments: bool = ..., image_repository_path: _Optional[str] = ..., params: _Optional[_Mapping[str, str]] = ..., pipeline_branch: _Optional[str] = ..., enable_pull_request_builds: bool = ...) -> None: ...

class ServiceIngressConfiguration(_message.Message):
    __slots__ = ("enabled", "dns_domain_id")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DNS_DOMAIN_ID_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    dns_domain_id: str
    def __init__(self, enabled: bool = ..., dns_domain_id: _Optional[str] = ...) -> None: ...
