from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from cloud.planton.apis.infrahub.iacmodule.v1 import git_repo_pb2 as _git_repo_pb2
from cloud.planton.apis.infrahub.iacmodule.v1 import pulumi_pb2 as _pulumi_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_provider_pb2 as _cloud_resource_provider_pb2
from project.planton.shared import iac_pb2 as _iac_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IacModuleSpec(_message.Message):
    __slots__ = ("selector", "cloud_resource_kind", "provisioner", "is_official", "description", "provider", "provider_icon_url", "icon_url", "git_repo", "project_runtime", "is_ready")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    PROVISIONER_FIELD_NUMBER: _ClassVar[int]
    IS_OFFICIAL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ICON_URL_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_FIELD_NUMBER: _ClassVar[int]
    PROJECT_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    IS_READY_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    provisioner: _iac_pb2.IacProvisioner
    is_official: bool
    description: str
    provider: _cloud_resource_provider_pb2.CloudResourceProvider
    provider_icon_url: str
    icon_url: str
    git_repo: _git_repo_pb2.IacModuleGitRepo
    project_runtime: _pulumi_pb2.PulumiProjectRuntime
    is_ready: bool
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., provisioner: _Optional[_Union[_iac_pb2.IacProvisioner, str]] = ..., is_official: bool = ..., description: _Optional[str] = ..., provider: _Optional[_Union[_cloud_resource_provider_pb2.CloudResourceProvider, str]] = ..., provider_icon_url: _Optional[str] = ..., icon_url: _Optional[str] = ..., git_repo: _Optional[_Union[_git_repo_pb2.IacModuleGitRepo, _Mapping]] = ..., project_runtime: _Optional[_Union[_pulumi_pb2.PulumiProjectRuntime, str]] = ..., is_ready: bool = ...) -> None: ...
