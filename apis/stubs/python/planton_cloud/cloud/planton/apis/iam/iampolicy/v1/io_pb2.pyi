from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from cloud.planton.apis.iam.iampolicy.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.iam.iampolicy.v1.rpcauthorization import iam_permission_pb2 as _iam_permission_pb2
from cloud.planton.apis.iam.iamrole.v1 import api_pb2 as _api_pb2_1
from cloud.planton.apis.iam.identityaccount.v1 import api_pb2 as _api_pb2_1_1
from cloud.planton.apis.iam.team.v1 import api_pb2 as _api_pb2_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IamPrincipal(_message.Message):
    __slots__ = ("id", "name", "email", "type", "picture_url")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    email: str
    type: str
    picture_url: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., type: _Optional[str] = ..., picture_url: _Optional[str] = ...) -> None: ...

class RoleAndInheritance(_message.Message):
    __slots__ = ("role", "owner_principal")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    OWNER_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    role: _api_pb2_1.IamRole
    owner_principal: IamPrincipal
    def __init__(self, role: _Optional[_Union[_api_pb2_1.IamRole, _Mapping]] = ..., owner_principal: _Optional[_Union[IamPrincipal, _Mapping]] = ...) -> None: ...

class IamPolicyByPrincipal(_message.Message):
    __slots__ = ("principal", "roles_and_inheritance")
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    ROLES_AND_INHERITANCE_FIELD_NUMBER: _ClassVar[int]
    principal: IamPrincipal
    roles_and_inheritance: _containers.RepeatedCompositeFieldContainer[RoleAndInheritance]
    def __init__(self, principal: _Optional[_Union[IamPrincipal, _Mapping]] = ..., roles_and_inheritance: _Optional[_Iterable[_Union[RoleAndInheritance, _Mapping]]] = ...) -> None: ...

class IamPolicy(_message.Message):
    __slots__ = ("principal", "role_and_inheritance")
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    ROLE_AND_INHERITANCE_FIELD_NUMBER: _ClassVar[int]
    principal: IamPrincipal
    role_and_inheritance: RoleAndInheritance
    def __init__(self, principal: _Optional[_Union[IamPrincipal, _Mapping]] = ..., role_and_inheritance: _Optional[_Union[RoleAndInheritance, _Mapping]] = ...) -> None: ...

class GetIamPolicyByApiResourceKindAndResourceIdInput(_message.Message):
    __slots__ = ("resource_kind", "resource_id", "show_inherited_policies")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    SHOW_INHERITED_POLICIES_FIELD_NUMBER: _ClassVar[int]
    resource_kind: str
    resource_id: str
    show_inherited_policies: bool
    def __init__(self, resource_kind: _Optional[str] = ..., resource_id: _Optional[str] = ..., show_inherited_policies: bool = ...) -> None: ...

class IamPoliciesByPrincipal(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[IamPolicyByPrincipal]
    def __init__(self, entries: _Optional[_Iterable[_Union[IamPolicyByPrincipal, _Mapping]]] = ...) -> None: ...

class AddIamPolicyInput(_message.Message):
    __slots__ = ("principals", "roles", "resource_kind", "resource_id")
    PRINCIPALS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    principals: _containers.RepeatedCompositeFieldContainer[IamPrincipal]
    roles: _containers.RepeatedCompositeFieldContainer[_api_pb2_1.IamRole]
    resource_kind: str
    resource_id: str
    def __init__(self, principals: _Optional[_Iterable[_Union[IamPrincipal, _Mapping]]] = ..., roles: _Optional[_Iterable[_Union[_api_pb2_1.IamRole, _Mapping]]] = ..., resource_kind: _Optional[str] = ..., resource_id: _Optional[str] = ...) -> None: ...

class RemoveIamPolicyInput(_message.Message):
    __slots__ = ("principal", "roles", "resource_kind", "resource_id")
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    principal: IamPrincipal
    roles: _containers.RepeatedCompositeFieldContainer[_api_pb2_1.IamRole]
    resource_kind: str
    resource_id: str
    def __init__(self, principal: _Optional[_Union[IamPrincipal, _Mapping]] = ..., roles: _Optional[_Iterable[_Union[_api_pb2_1.IamRole, _Mapping]]] = ..., resource_kind: _Optional[str] = ..., resource_id: _Optional[str] = ...) -> None: ...

class RemoveIamPoliciesInput(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[RemoveIamPolicyInput]
    def __init__(self, entries: _Optional[_Iterable[_Union[RemoveIamPolicyInput, _Mapping]]] = ...) -> None: ...

class IamPolicyByRole(_message.Message):
    __slots__ = ("role_owner_mapping", "principals")
    ROLE_OWNER_MAPPING_FIELD_NUMBER: _ClassVar[int]
    PRINCIPALS_FIELD_NUMBER: _ClassVar[int]
    role_owner_mapping: RoleAndInheritance
    principals: _containers.RepeatedCompositeFieldContainer[IamPrincipal]
    def __init__(self, role_owner_mapping: _Optional[_Union[RoleAndInheritance, _Mapping]] = ..., principals: _Optional[_Iterable[_Union[IamPrincipal, _Mapping]]] = ...) -> None: ...

class IamPoliciesByRole(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[IamPolicyByRole]
    def __init__(self, entries: _Optional[_Iterable[_Union[IamPolicyByRole, _Mapping]]] = ...) -> None: ...

class UpdateIamPolicyInput(_message.Message):
    __slots__ = ("principal", "roles", "resource_kind", "resource_id")
    PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    principal: IamPrincipal
    roles: _containers.RepeatedCompositeFieldContainer[_api_pb2_1.IamRole]
    resource_kind: str
    resource_id: str
    def __init__(self, principal: _Optional[_Union[IamPrincipal, _Mapping]] = ..., roles: _Optional[_Iterable[_Union[_api_pb2_1.IamRole, _Mapping]]] = ..., resource_kind: _Optional[str] = ..., resource_id: _Optional[str] = ...) -> None: ...

class AuthorizationInput(_message.Message):
    __slots__ = ("tuple", "contextual_tuples")
    TUPLE_FIELD_NUMBER: _ClassVar[int]
    CONTEXTUAL_TUPLES_FIELD_NUMBER: _ClassVar[int]
    tuple: _api_pb2.FgaTuple
    contextual_tuples: _containers.RepeatedCompositeFieldContainer[_api_pb2.FgaTuple]
    def __init__(self, tuple: _Optional[_Union[_api_pb2.FgaTuple, _Mapping]] = ..., contextual_tuples: _Optional[_Iterable[_Union[_api_pb2.FgaTuple, _Mapping]]] = ...) -> None: ...

class ListAuthorizedResourceIdsInput(_message.Message):
    __slots__ = ("tuple", "contextual_tuples")
    TUPLE_FIELD_NUMBER: _ClassVar[int]
    CONTEXTUAL_TUPLES_FIELD_NUMBER: _ClassVar[int]
    tuple: _api_pb2.FgaTuple
    contextual_tuples: _containers.RepeatedCompositeFieldContainer[_api_pb2.FgaTuple]
    def __init__(self, tuple: _Optional[_Union[_api_pb2.FgaTuple, _Mapping]] = ..., contextual_tuples: _Optional[_Iterable[_Union[_api_pb2.FgaTuple, _Mapping]]] = ...) -> None: ...

class IsAuthorized(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: bool = ...) -> None: ...

class AuthorizedResourceIds(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class GetIamPolicyByApiResourceKindAndResourceIdAndIdentityAccountIdInput(_message.Message):
    __slots__ = ("resource_kind", "resource_id", "identity_account_id")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    resource_kind: str
    resource_id: str
    identity_account_id: str
    def __init__(self, resource_kind: _Optional[str] = ..., resource_id: _Optional[str] = ..., identity_account_id: _Optional[str] = ...) -> None: ...

class AuthorizedUserIds(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class ListAuthorizedUserIdsInput(_message.Message):
    __slots__ = ("user_type", "user_relation", "relation", "object_type", "object_id")
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_RELATION_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    user_type: _api_resource_kind_pb2.ApiResourceKind
    user_relation: str
    relation: _iam_permission_pb2.ApiResourceIamPermission
    object_type: _api_resource_kind_pb2.ApiResourceKind
    object_id: str
    def __init__(self, user_type: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., user_relation: _Optional[str] = ..., relation: _Optional[_Union[_iam_permission_pb2.ApiResourceIamPermission, str]] = ..., object_type: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., object_id: _Optional[str] = ...) -> None: ...

class RevokeMemberAccessOnOrgInput(_message.Message):
    __slots__ = ("identity_account_id", "org")
    IDENTITY_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    identity_account_id: str
    org: str
    def __init__(self, identity_account_id: _Optional[str] = ..., org: _Optional[str] = ...) -> None: ...

class FindByOrgRequest(_message.Message):
    __slots__ = ("org", "page")
    ORG_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    org: str
    page: _pagination_pb2.PageInfo
    def __init__(self, org: _Optional[str] = ..., page: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ...) -> None: ...

class FindByEnvInput(_message.Message):
    __slots__ = ("org", "env", "page")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    page: _pagination_pb2.PageInfo
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., page: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ...) -> None: ...

class MemberWithRoles(_message.Message):
    __slots__ = ("identity_account", "roles_and_inheritance", "teams")
    IDENTITY_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ROLES_AND_INHERITANCE_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    identity_account: _api_pb2_1_1.IdentityAccount
    roles_and_inheritance: _containers.RepeatedCompositeFieldContainer[RoleAndInheritance]
    teams: _containers.RepeatedCompositeFieldContainer[_api_pb2_1_1_1.Team]
    def __init__(self, identity_account: _Optional[_Union[_api_pb2_1_1.IdentityAccount, _Mapping]] = ..., roles_and_inheritance: _Optional[_Iterable[_Union[RoleAndInheritance, _Mapping]]] = ..., teams: _Optional[_Iterable[_Union[_api_pb2_1_1_1.Team, _Mapping]]] = ...) -> None: ...

class MemberWithRolesList(_message.Message):
    __slots__ = ("entries", "total_pages")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[MemberWithRoles]
    total_pages: int
    def __init__(self, entries: _Optional[_Iterable[_Union[MemberWithRoles, _Mapping]]] = ..., total_pages: _Optional[int] = ...) -> None: ...

class CountByOrgRequest(_message.Message):
    __slots__ = ("org",)
    ORG_FIELD_NUMBER: _ClassVar[int]
    org: str
    def __init__(self, org: _Optional[str] = ...) -> None: ...

class CountByEnvInput(_message.Message):
    __slots__ = ("org", "env")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...

class UsersCount(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class TeamWithRoles(_message.Message):
    __slots__ = ("team", "roles_and_inheritance")
    TEAM_FIELD_NUMBER: _ClassVar[int]
    ROLES_AND_INHERITANCE_FIELD_NUMBER: _ClassVar[int]
    team: _api_pb2_1_1_1.Team
    roles_and_inheritance: _containers.RepeatedCompositeFieldContainer[RoleAndInheritance]
    def __init__(self, team: _Optional[_Union[_api_pb2_1_1_1.Team, _Mapping]] = ..., roles_and_inheritance: _Optional[_Iterable[_Union[RoleAndInheritance, _Mapping]]] = ...) -> None: ...

class TeamWithRolesList(_message.Message):
    __slots__ = ("entries", "total_pages")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[TeamWithRoles]
    total_pages: int
    def __init__(self, entries: _Optional[_Iterable[_Union[TeamWithRoles, _Mapping]]] = ..., total_pages: _Optional[int] = ...) -> None: ...

class InviteMemberInput(_message.Message):
    __slots__ = ("identity_account_id",)
    IDENTITY_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    identity_account_id: str
    def __init__(self, identity_account_id: _Optional[str] = ...) -> None: ...

class ListObjectIdsByRoleInput(_message.Message):
    __slots__ = ("user_type", "user_id", "relation", "object_type")
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    user_type: _api_resource_kind_pb2.ApiResourceKind
    user_id: str
    relation: str
    object_type: _api_resource_kind_pb2.ApiResourceKind
    def __init__(self, user_type: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., user_id: _Optional[str] = ..., relation: _Optional[str] = ..., object_type: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ...) -> None: ...
