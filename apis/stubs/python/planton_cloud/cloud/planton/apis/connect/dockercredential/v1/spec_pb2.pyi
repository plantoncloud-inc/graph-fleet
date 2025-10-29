from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DockerRepoProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    docker_repo_provider_unspecified: _ClassVar[DockerRepoProvider]
    gcp_artifact_registry: _ClassVar[DockerRepoProvider]
    aws_elastic_container_registry: _ClassVar[DockerRepoProvider]
    azure_container_registry: _ClassVar[DockerRepoProvider]
    jfrog_artifactory: _ClassVar[DockerRepoProvider]
    github_container_registry: _ClassVar[DockerRepoProvider]
docker_repo_provider_unspecified: DockerRepoProvider
gcp_artifact_registry: DockerRepoProvider
aws_elastic_container_registry: DockerRepoProvider
azure_container_registry: DockerRepoProvider
jfrog_artifactory: DockerRepoProvider
github_container_registry: DockerRepoProvider

class DockerCredentialSpec(_message.Message):
    __slots__ = ("provider", "gcp_artifact_registry", "aws_elastic_container_registry", "azure_container_registry", "jfrog_artifactory", "github_container_registry")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GCP_ARTIFACT_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    AWS_ELASTIC_CONTAINER_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    AZURE_CONTAINER_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    JFROG_ARTIFACTORY_FIELD_NUMBER: _ClassVar[int]
    GITHUB_CONTAINER_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    provider: DockerRepoProvider
    gcp_artifact_registry: DockerCredentialGcpArtifactRegistry
    aws_elastic_container_registry: DockerCredentialAwsElasticContainerRegistry
    azure_container_registry: DockerCredentialAzureContainerRegistry
    jfrog_artifactory: DockerCredentialJfrogArtifactory
    github_container_registry: DockerCredentialGithubContainerRegistry
    def __init__(self, provider: _Optional[_Union[DockerRepoProvider, str]] = ..., gcp_artifact_registry: _Optional[_Union[DockerCredentialGcpArtifactRegistry, _Mapping]] = ..., aws_elastic_container_registry: _Optional[_Union[DockerCredentialAwsElasticContainerRegistry, _Mapping]] = ..., azure_container_registry: _Optional[_Union[DockerCredentialAzureContainerRegistry, _Mapping]] = ..., jfrog_artifactory: _Optional[_Union[DockerCredentialJfrogArtifactory, _Mapping]] = ..., github_container_registry: _Optional[_Union[DockerCredentialGithubContainerRegistry, _Mapping]] = ...) -> None: ...

class DockerCredentialGcpArtifactRegistry(_message.Message):
    __slots__ = ("gcp_project_id", "gcp_region", "service_account_key_base64", "gcp_artifact_registry_repo_name")
    GCP_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    GCP_REGION_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    GCP_ARTIFACT_REGISTRY_REPO_NAME_FIELD_NUMBER: _ClassVar[int]
    gcp_project_id: str
    gcp_region: str
    service_account_key_base64: str
    gcp_artifact_registry_repo_name: str
    def __init__(self, gcp_project_id: _Optional[str] = ..., gcp_region: _Optional[str] = ..., service_account_key_base64: _Optional[str] = ..., gcp_artifact_registry_repo_name: _Optional[str] = ...) -> None: ...

class DockerCredentialAwsElasticContainerRegistry(_message.Message):
    __slots__ = ("account_id", "access_key_id", "secret_access_key", "region")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    access_key_id: str
    secret_access_key: str
    region: str
    def __init__(self, account_id: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ..., region: _Optional[str] = ...) -> None: ...

class DockerCredentialAzureContainerRegistry(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DockerCredentialJfrogArtifactory(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DockerCredentialGithubContainerRegistry(_message.Message):
    __slots__ = ("github_username", "personal_access_token")
    GITHUB_USERNAME_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    github_username: str
    personal_access_token: str
    def __init__(self, github_username: _Optional[str] = ..., personal_access_token: _Optional[str] = ...) -> None: ...
