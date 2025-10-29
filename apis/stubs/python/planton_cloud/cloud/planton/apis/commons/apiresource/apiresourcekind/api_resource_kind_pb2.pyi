from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_group_pb2 as _api_resource_group_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    api_resource_version_unspecified: _ClassVar[ApiResourceVersion]
    v1: _ClassVar[ApiResourceVersion]
    v2: _ClassVar[ApiResourceVersion]

class CloudResourceCredentialKindMapping(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    cloud_resource_credential_kind_mapping_unspecified: _ClassVar[CloudResourceCredentialKindMapping]
    atlas: _ClassVar[CloudResourceCredentialKindMapping]
    aws: _ClassVar[CloudResourceCredentialKindMapping]
    azure: _ClassVar[CloudResourceCredentialKindMapping]
    civo: _ClassVar[CloudResourceCredentialKindMapping]
    cloudflare: _ClassVar[CloudResourceCredentialKindMapping]
    confluent: _ClassVar[CloudResourceCredentialKindMapping]
    digital_ocean: _ClassVar[CloudResourceCredentialKindMapping]
    gcp: _ClassVar[CloudResourceCredentialKindMapping]
    kubernetes: _ClassVar[CloudResourceCredentialKindMapping]
    snowflake: _ClassVar[CloudResourceCredentialKindMapping]

class CredentialCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    credential_category_unspecified: _ClassVar[CredentialCategory]
    iac_backend_credential: _ClassVar[CredentialCategory]
    provider_credential: _ClassVar[CredentialCategory]
    package_credential: _ClassVar[CredentialCategory]
    scm_credential: _ClassVar[CredentialCategory]

class PlatformIdValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    platform_id_value_unspecified: _ClassVar[PlatformIdValue]
    planton_cloud: _ClassVar[PlatformIdValue]

class ApiResourceKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    unspecified: _ClassVar[ApiResourceKind]
    test_api_resource: _ClassVar[ApiResourceKind]
    test_credential_resource: _ClassVar[ApiResourceKind]
    platform: _ClassVar[ApiResourceKind]
    identity_account: _ClassVar[ApiResourceKind]
    organization: _ClassVar[ApiResourceKind]
    team: _ClassVar[ApiResourceKind]
    environment: _ClassVar[ApiResourceKind]
    service: _ClassVar[ApiResourceKind]
    variables_group: _ClassVar[ApiResourceKind]
    secrets_group: _ClassVar[ApiResourceKind]
    dns_domain: _ClassVar[ApiResourceKind]
    api_resource_version: _ClassVar[ApiResourceKind]
    github_action: _ClassVar[ApiResourceKind]
    github_workflow: _ClassVar[ApiResourceKind]
    cookie_cutter_template: _ClassVar[ApiResourceKind]
    chat: _ClassVar[ApiResourceKind]
    chat_message: _ClassVar[ApiResourceKind]
    flow_control_policy: _ClassVar[ApiResourceKind]
    iac_module: _ClassVar[ApiResourceKind]
    pipeline: _ClassVar[ApiResourceKind]
    provider_credential_mapping: _ClassVar[ApiResourceKind]
    iac_provisioner_mapping: _ClassVar[ApiResourceKind]
    billing_account: _ClassVar[ApiResourceKind]
    quick_action: _ClassVar[ApiResourceKind]
    deployment_component: _ClassVar[ApiResourceKind]
    stack_job: _ClassVar[ApiResourceKind]
    stack_job_runner: _ClassVar[ApiResourceKind]
    infra_chart: _ClassVar[ApiResourceKind]
    infra_project: _ClassVar[ApiResourceKind]
    agent: _ClassVar[ApiResourceKind]
    api_key: _ClassVar[ApiResourceKind]
    iam_role: _ClassVar[ApiResourceKind]
    promotion_policy: _ClassVar[ApiResourceKind]
    infra_pipeline: _ClassVar[ApiResourceKind]
    secret: _ClassVar[ApiResourceKind]
    secret_version: _ClassVar[ApiResourceKind]
    cloud_resource: _ClassVar[ApiResourceKind]
    session: _ClassVar[ApiResourceKind]
    execution: _ClassVar[ApiResourceKind]
    aws_credential: _ClassVar[ApiResourceKind]
    gcp_credential: _ClassVar[ApiResourceKind]
    azure_credential: _ClassVar[ApiResourceKind]
    kubernetes_cluster_credential: _ClassVar[ApiResourceKind]
    mongodb_atlas_credential: _ClassVar[ApiResourceKind]
    confluent_credential: _ClassVar[ApiResourceKind]
    snowflake_credential: _ClassVar[ApiResourceKind]
    pulumi_backend_credential: _ClassVar[ApiResourceKind]
    terraform_backend_credential: _ClassVar[ApiResourceKind]
    github_credential: _ClassVar[ApiResourceKind]
    gitlab_credential: _ClassVar[ApiResourceKind]
    docker_credential: _ClassVar[ApiResourceKind]
    maven_credential: _ClassVar[ApiResourceKind]
    git_credential: _ClassVar[ApiResourceKind]
    chat_gpt_credential: _ClassVar[ApiResourceKind]
    npm_credential: _ClassVar[ApiResourceKind]
    digital_ocean_credential: _ClassVar[ApiResourceKind]
    civo_credential: _ClassVar[ApiResourceKind]
    cloudflare_credential: _ClassVar[ApiResourceKind]
    iam_policy: _ClassVar[ApiResourceKind]
api_resource_version_unspecified: ApiResourceVersion
v1: ApiResourceVersion
v2: ApiResourceVersion
cloud_resource_credential_kind_mapping_unspecified: CloudResourceCredentialKindMapping
atlas: CloudResourceCredentialKindMapping
aws: CloudResourceCredentialKindMapping
azure: CloudResourceCredentialKindMapping
civo: CloudResourceCredentialKindMapping
cloudflare: CloudResourceCredentialKindMapping
confluent: CloudResourceCredentialKindMapping
digital_ocean: CloudResourceCredentialKindMapping
gcp: CloudResourceCredentialKindMapping
kubernetes: CloudResourceCredentialKindMapping
snowflake: CloudResourceCredentialKindMapping
credential_category_unspecified: CredentialCategory
iac_backend_credential: CredentialCategory
provider_credential: CredentialCategory
package_credential: CredentialCategory
scm_credential: CredentialCategory
platform_id_value_unspecified: PlatformIdValue
planton_cloud: PlatformIdValue
unspecified: ApiResourceKind
test_api_resource: ApiResourceKind
test_credential_resource: ApiResourceKind
platform: ApiResourceKind
identity_account: ApiResourceKind
organization: ApiResourceKind
team: ApiResourceKind
environment: ApiResourceKind
service: ApiResourceKind
variables_group: ApiResourceKind
secrets_group: ApiResourceKind
dns_domain: ApiResourceKind
api_resource_version: ApiResourceKind
github_action: ApiResourceKind
github_workflow: ApiResourceKind
cookie_cutter_template: ApiResourceKind
chat: ApiResourceKind
chat_message: ApiResourceKind
flow_control_policy: ApiResourceKind
iac_module: ApiResourceKind
pipeline: ApiResourceKind
provider_credential_mapping: ApiResourceKind
iac_provisioner_mapping: ApiResourceKind
billing_account: ApiResourceKind
quick_action: ApiResourceKind
deployment_component: ApiResourceKind
stack_job: ApiResourceKind
stack_job_runner: ApiResourceKind
infra_chart: ApiResourceKind
infra_project: ApiResourceKind
agent: ApiResourceKind
api_key: ApiResourceKind
iam_role: ApiResourceKind
promotion_policy: ApiResourceKind
infra_pipeline: ApiResourceKind
secret: ApiResourceKind
secret_version: ApiResourceKind
cloud_resource: ApiResourceKind
session: ApiResourceKind
execution: ApiResourceKind
aws_credential: ApiResourceKind
gcp_credential: ApiResourceKind
azure_credential: ApiResourceKind
kubernetes_cluster_credential: ApiResourceKind
mongodb_atlas_credential: ApiResourceKind
confluent_credential: ApiResourceKind
snowflake_credential: ApiResourceKind
pulumi_backend_credential: ApiResourceKind
terraform_backend_credential: ApiResourceKind
github_credential: ApiResourceKind
gitlab_credential: ApiResourceKind
docker_credential: ApiResourceKind
maven_credential: ApiResourceKind
git_credential: ApiResourceKind
chat_gpt_credential: ApiResourceKind
npm_credential: ApiResourceKind
digital_ocean_credential: ApiResourceKind
civo_credential: ApiResourceKind
cloudflare_credential: ApiResourceKind
iam_policy: ApiResourceKind
KIND_META_FIELD_NUMBER: _ClassVar[int]
kind_meta: _descriptor.FieldDescriptor
OWNER_FIELD_NUMBER: _ClassVar[int]
owner: _descriptor.FieldDescriptor
PROVIDER_CREDENTIAL_KIND_FIELD_NUMBER: _ClassVar[int]
provider_credential_kind: _descriptor.FieldDescriptor

class ApiResourceKindMeta(_message.Message):
    __slots__ = ("group", "version", "name", "display_name", "id_prefix", "is_versioned", "not_search_indexed", "is_credential", "credential_category")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_PREFIX_FIELD_NUMBER: _ClassVar[int]
    IS_VERSIONED_FIELD_NUMBER: _ClassVar[int]
    NOT_SEARCH_INDEXED_FIELD_NUMBER: _ClassVar[int]
    IS_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    group: _api_resource_group_pb2.ApiResourceGroup
    version: ApiResourceVersion
    name: str
    display_name: str
    id_prefix: str
    is_versioned: bool
    not_search_indexed: bool
    is_credential: bool
    credential_category: CredentialCategory
    def __init__(self, group: _Optional[_Union[_api_resource_group_pb2.ApiResourceGroup, str]] = ..., version: _Optional[_Union[ApiResourceVersion, str]] = ..., name: _Optional[str] = ..., display_name: _Optional[str] = ..., id_prefix: _Optional[str] = ..., is_versioned: bool = ..., not_search_indexed: bool = ..., is_credential: bool = ..., credential_category: _Optional[_Union[CredentialCategory, str]] = ...) -> None: ...

class ApiResourceOwnerInfo(_message.Message):
    __slots__ = ("resource_kind", "kind_field_path", "id_field_path")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    resource_kind: ApiResourceKind
    kind_field_path: str
    id_field_path: str
    def __init__(self, resource_kind: _Optional[_Union[ApiResourceKind, str]] = ..., kind_field_path: _Optional[str] = ..., id_field_path: _Optional[str] = ...) -> None: ...
