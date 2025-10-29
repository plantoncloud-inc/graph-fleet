from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceAuthorizationGroup(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    api_resource_authorization_group_unspecified: _ClassVar[ApiResourceAuthorizationGroup]
    credential_resource: _ClassVar[ApiResourceAuthorizationGroup]

class ApiResourceIamPermission(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    unspecified: _ClassVar[ApiResourceIamPermission]
    create: _ClassVar[ApiResourceIamPermission]
    delete: _ClassVar[ApiResourceIamPermission]
    get: _ClassVar[ApiResourceIamPermission]
    restore: _ClassVar[ApiResourceIamPermission]
    update: _ClassVar[ApiResourceIamPermission]
    list_associates: _ClassVar[ApiResourceIamPermission]
    login_to_back_office: _ClassVar[ApiResourceIamPermission]
    operator: _ClassVar[ApiResourceIamPermission]
    back_office_admin: _ClassVar[ApiResourceIamPermission]
    platform: _ClassVar[ApiResourceIamPermission]
    use_to_create: _ClassVar[ApiResourceIamPermission]
    iam_policy_update: _ClassVar[ApiResourceIamPermission]
    iam_policy_get: _ClassVar[ApiResourceIamPermission]
    owner: _ClassVar[ApiResourceIamPermission]
    identity_account_in_context: _ClassVar[ApiResourceIamPermission]
    public_view: _ClassVar[ApiResourceIamPermission]
    agent_create: _ClassVar[ApiResourceIamPermission]
    cloud_resource_create: _ClassVar[ApiResourceIamPermission]
    credential_resource_create: _ClassVar[ApiResourceIamPermission]
    dns_domain_create: _ClassVar[ApiResourceIamPermission]
    environment_create: _ClassVar[ApiResourceIamPermission]
    infra_project_create: _ClassVar[ApiResourceIamPermission]
    secrets_group_create: _ClassVar[ApiResourceIamPermission]
    service_create: _ClassVar[ApiResourceIamPermission]
    team_create: _ClassVar[ApiResourceIamPermission]
    variables_group_create: _ClassVar[ApiResourceIamPermission]
    member: _ClassVar[ApiResourceIamPermission]
    share: _ClassVar[ApiResourceIamPermission]
api_resource_authorization_group_unspecified: ApiResourceAuthorizationGroup
credential_resource: ApiResourceAuthorizationGroup
unspecified: ApiResourceIamPermission
create: ApiResourceIamPermission
delete: ApiResourceIamPermission
get: ApiResourceIamPermission
restore: ApiResourceIamPermission
update: ApiResourceIamPermission
list_associates: ApiResourceIamPermission
login_to_back_office: ApiResourceIamPermission
operator: ApiResourceIamPermission
back_office_admin: ApiResourceIamPermission
platform: ApiResourceIamPermission
use_to_create: ApiResourceIamPermission
iam_policy_update: ApiResourceIamPermission
iam_policy_get: ApiResourceIamPermission
owner: ApiResourceIamPermission
identity_account_in_context: ApiResourceIamPermission
public_view: ApiResourceIamPermission
agent_create: ApiResourceIamPermission
cloud_resource_create: ApiResourceIamPermission
credential_resource_create: ApiResourceIamPermission
dns_domain_create: ApiResourceIamPermission
environment_create: ApiResourceIamPermission
infra_project_create: ApiResourceIamPermission
secrets_group_create: ApiResourceIamPermission
service_create: ApiResourceIamPermission
team_create: ApiResourceIamPermission
variables_group_create: ApiResourceIamPermission
member: ApiResourceIamPermission
share: ApiResourceIamPermission
