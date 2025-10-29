from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpArtifactRegistryRepoFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    gcp_artifact_registry_repo_format_unspecified: _ClassVar[GcpArtifactRegistryRepoFormat]
    DOCKER: _ClassVar[GcpArtifactRegistryRepoFormat]
    GENERIC: _ClassVar[GcpArtifactRegistryRepoFormat]
    GO: _ClassVar[GcpArtifactRegistryRepoFormat]
    KUBEFLOW: _ClassVar[GcpArtifactRegistryRepoFormat]
    MAVEN: _ClassVar[GcpArtifactRegistryRepoFormat]
    NPM: _ClassVar[GcpArtifactRegistryRepoFormat]
    PYTHON: _ClassVar[GcpArtifactRegistryRepoFormat]
    YUM: _ClassVar[GcpArtifactRegistryRepoFormat]
gcp_artifact_registry_repo_format_unspecified: GcpArtifactRegistryRepoFormat
DOCKER: GcpArtifactRegistryRepoFormat
GENERIC: GcpArtifactRegistryRepoFormat
GO: GcpArtifactRegistryRepoFormat
KUBEFLOW: GcpArtifactRegistryRepoFormat
MAVEN: GcpArtifactRegistryRepoFormat
NPM: GcpArtifactRegistryRepoFormat
PYTHON: GcpArtifactRegistryRepoFormat
YUM: GcpArtifactRegistryRepoFormat

class GcpArtifactRegistryRepoSpec(_message.Message):
    __slots__ = ("repo_format", "project_id", "region", "enable_public_access")
    REPO_FORMAT_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PUBLIC_ACCESS_FIELD_NUMBER: _ClassVar[int]
    repo_format: GcpArtifactRegistryRepoFormat
    project_id: str
    region: str
    enable_public_access: bool
    def __init__(self, repo_format: _Optional[_Union[GcpArtifactRegistryRepoFormat, str]] = ..., project_id: _Optional[str] = ..., region: _Optional[str] = ..., enable_public_access: bool = ...) -> None: ...
