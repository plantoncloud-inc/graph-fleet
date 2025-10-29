from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from cloud.planton.apis.iam.iamrole.v1 import api_pb2 as _api_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserInvitationStatusType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    user_invitation_status_type_unspecified: _ClassVar[UserInvitationStatusType]
    pending: _ClassVar[UserInvitationStatusType]
    accepted: _ClassVar[UserInvitationStatusType]
    removed: _ClassVar[UserInvitationStatusType]
user_invitation_status_type_unspecified: UserInvitationStatusType
pending: UserInvitationStatusType
accepted: UserInvitationStatusType
removed: UserInvitationStatusType

class CreateUserInvitationInput(_message.Message):
    __slots__ = ("org", "email", "iam_role_ids")
    ORG_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    IAM_ROLE_IDS_FIELD_NUMBER: _ClassVar[int]
    org: str
    email: str
    iam_role_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, org: _Optional[str] = ..., email: _Optional[str] = ..., iam_role_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class UserInvitation(_message.Message):
    __slots__ = ("id", "org", "identity_account_id", "email", "iam_roles", "token", "invitation_url", "status", "audit_info")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    IAM_ROLES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    INVITATION_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AUDIT_INFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    org: str
    identity_account_id: str
    email: str
    iam_roles: _containers.RepeatedCompositeFieldContainer[_api_pb2.IamRole]
    token: str
    invitation_url: str
    status: UserInvitationStatusType
    audit_info: _status_pb2.ApiResourceAuditInfo
    def __init__(self, id: _Optional[str] = ..., org: _Optional[str] = ..., identity_account_id: _Optional[str] = ..., email: _Optional[str] = ..., iam_roles: _Optional[_Iterable[_Union[_api_pb2.IamRole, _Mapping]]] = ..., token: _Optional[str] = ..., invitation_url: _Optional[str] = ..., status: _Optional[_Union[UserInvitationStatusType, str]] = ..., audit_info: _Optional[_Union[_status_pb2.ApiResourceAuditInfo, _Mapping]] = ...) -> None: ...

class UpdateUserInvitationStatusInput(_message.Message):
    __slots__ = ("token", "status")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    token: str
    status: UserInvitationStatusType
    def __init__(self, token: _Optional[str] = ..., status: _Optional[_Union[UserInvitationStatusType, str]] = ...) -> None: ...

class FindUserInvitationsByOrgByStatusInput(_message.Message):
    __slots__ = ("org", "status")
    ORG_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    org: str
    status: UserInvitationStatusType
    def __init__(self, org: _Optional[str] = ..., status: _Optional[_Union[UserInvitationStatusType, str]] = ...) -> None: ...

class UserInvitations(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[UserInvitation]
    def __init__(self, entries: _Optional[_Iterable[_Union[UserInvitation, _Mapping]]] = ...) -> None: ...

class FindUserInvitationByTokenInput(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...
