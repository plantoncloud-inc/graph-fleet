from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareZeroTrustPolicyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALLOW: _ClassVar[CloudflareZeroTrustPolicyType]
    BLOCK: _ClassVar[CloudflareZeroTrustPolicyType]
ALLOW: CloudflareZeroTrustPolicyType
BLOCK: CloudflareZeroTrustPolicyType

class CloudflareZeroTrustAccessApplicationSpec(_message.Message):
    __slots__ = ("application_name", "zone_id", "hostname", "policy_type", "allowed_emails", "session_duration_minutes", "require_mfa", "allowed_google_groups")
    APPLICATION_NAME_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_EMAILS_FIELD_NUMBER: _ClassVar[int]
    SESSION_DURATION_MINUTES_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_MFA_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_GOOGLE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    application_name: str
    zone_id: str
    hostname: str
    policy_type: CloudflareZeroTrustPolicyType
    allowed_emails: _containers.RepeatedScalarFieldContainer[str]
    session_duration_minutes: int
    require_mfa: bool
    allowed_google_groups: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, application_name: _Optional[str] = ..., zone_id: _Optional[str] = ..., hostname: _Optional[str] = ..., policy_type: _Optional[_Union[CloudflareZeroTrustPolicyType, str]] = ..., allowed_emails: _Optional[_Iterable[str]] = ..., session_duration_minutes: _Optional[int] = ..., require_mfa: bool = ..., allowed_google_groups: _Optional[_Iterable[str]] = ...) -> None: ...
