import datetime

from cloud.planton.apis.agentfleet.agent.v1 import spec_pb2 as _spec_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from cloud.planton.apis.infrahub.infraproject.v1 import spec_pb2 as _spec_pb2_1
from cloud.planton.apis.integration.vcs import provider_pb2 as _provider_pb2
from cloud.planton.apis.search.quickaction.v1 import spec_pb2 as _spec_pb2_1_1
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_provider_pb2 as _cloud_resource_provider_pb2
from project.planton.shared import iac_pb2 as _iac_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceSearchRecord(_message.Message):
    __slots__ = ("id", "name", "kind", "org", "env", "tags", "created_by", "created_at", "selector_kind", "selector_id", "email", "icon_url", "quick_action_api_resource_kind", "quick_action_type", "iac_provisioner", "is_official_iac_module", "cloud_resource_provider", "cloud_resource_provider_icon_url", "cloud_resource_kind", "description", "is_ready", "source_code_web_url", "git_provider", "git_repo_name", "github_organization", "gitlab_group", "infra_project_source", "agent_framework", "agent_runtime", "slug")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_KIND_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    QUICK_ACTION_API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    QUICK_ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    IAC_PROVISIONER_FIELD_NUMBER: _ClassVar[int]
    IS_OFFICIAL_IAC_MODULE_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_PROVIDER_ICON_URL_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_READY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CODE_WEB_URL_FIELD_NUMBER: _ClassVar[int]
    GIT_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_NAME_FIELD_NUMBER: _ClassVar[int]
    GITHUB_ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    GITLAB_GROUP_FIELD_NUMBER: _ClassVar[int]
    INFRA_PROJECT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    AGENT_FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    AGENT_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    kind: _api_resource_kind_pb2.ApiResourceKind
    org: str
    env: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    created_by: _status_pb2.ApiResourceAuditActor
    created_at: _timestamp_pb2.Timestamp
    selector_kind: _api_resource_kind_pb2.ApiResourceKind
    selector_id: str
    email: str
    icon_url: str
    quick_action_api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    quick_action_type: _spec_pb2_1_1.QuickActionType
    iac_provisioner: _iac_pb2.IacProvisioner
    is_official_iac_module: bool
    cloud_resource_provider: _cloud_resource_provider_pb2.CloudResourceProvider
    cloud_resource_provider_icon_url: str
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    description: str
    is_ready: bool
    source_code_web_url: str
    git_provider: _provider_pb2.GitRepoProvider
    git_repo_name: str
    github_organization: str
    gitlab_group: str
    infra_project_source: _spec_pb2_1.InfraProjectSource
    agent_framework: _spec_pb2.AgentFramework
    agent_runtime: _spec_pb2.AgentRuntime
    slug: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., org: _Optional[str] = ..., env: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., created_by: _Optional[_Union[_status_pb2.ApiResourceAuditActor, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., selector_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., selector_id: _Optional[str] = ..., email: _Optional[str] = ..., icon_url: _Optional[str] = ..., quick_action_api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., quick_action_type: _Optional[_Union[_spec_pb2_1_1.QuickActionType, str]] = ..., iac_provisioner: _Optional[_Union[_iac_pb2.IacProvisioner, str]] = ..., is_official_iac_module: bool = ..., cloud_resource_provider: _Optional[_Union[_cloud_resource_provider_pb2.CloudResourceProvider, str]] = ..., cloud_resource_provider_icon_url: _Optional[str] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., description: _Optional[str] = ..., is_ready: bool = ..., source_code_web_url: _Optional[str] = ..., git_provider: _Optional[_Union[_provider_pb2.GitRepoProvider, str]] = ..., git_repo_name: _Optional[str] = ..., github_organization: _Optional[str] = ..., gitlab_group: _Optional[str] = ..., infra_project_source: _Optional[_Union[_spec_pb2_1.InfraProjectSource, str]] = ..., agent_framework: _Optional[_Union[_spec_pb2.AgentFramework, str]] = ..., agent_runtime: _Optional[_Union[_spec_pb2.AgentRuntime, str]] = ..., slug: _Optional[str] = ...) -> None: ...
