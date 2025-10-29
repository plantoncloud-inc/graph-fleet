from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MavenRepoProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    maven_repo_provider_unspecified: _ClassVar[MavenRepoProvider]
    gcp_artifact_registry: _ClassVar[MavenRepoProvider]
    jfrog_artifactory: _ClassVar[MavenRepoProvider]
    github_packages: _ClassVar[MavenRepoProvider]
maven_repo_provider_unspecified: MavenRepoProvider
gcp_artifact_registry: MavenRepoProvider
jfrog_artifactory: MavenRepoProvider
github_packages: MavenRepoProvider

class MavenCredentialSpec(_message.Message):
    __slots__ = ("provider", "gcp_artifact_registry", "jfrog_artifactory", "github_packages")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GCP_ARTIFACT_REGISTRY_FIELD_NUMBER: _ClassVar[int]
    JFROG_ARTIFACTORY_FIELD_NUMBER: _ClassVar[int]
    GITHUB_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    provider: MavenRepoProvider
    gcp_artifact_registry: MavenCredentialGcpArtifactRegistry
    jfrog_artifactory: MavenCredentialJfrogArtifactory
    github_packages: MavenCredentialGithubPackages
    def __init__(self, provider: _Optional[_Union[MavenRepoProvider, str]] = ..., gcp_artifact_registry: _Optional[_Union[MavenCredentialGcpArtifactRegistry, _Mapping]] = ..., jfrog_artifactory: _Optional[_Union[MavenCredentialJfrogArtifactory, _Mapping]] = ..., github_packages: _Optional[_Union[MavenCredentialGithubPackages, _Mapping]] = ...) -> None: ...

class MavenCredentialGcpArtifactRegistry(_message.Message):
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

class MavenCredentialJfrogArtifactory(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MavenCredentialGithubPackages(_message.Message):
    __slots__ = ("github_username", "personal_access_token")
    GITHUB_USERNAME_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    github_username: str
    personal_access_token: str
    def __init__(self, github_username: _Optional[str] = ..., personal_access_token: _Optional[str] = ...) -> None: ...
