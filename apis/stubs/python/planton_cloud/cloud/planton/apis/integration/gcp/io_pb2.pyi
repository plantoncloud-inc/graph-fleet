from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AuthorizeGcpCloudAccountInput(_message.Message):
    __slots__ = ("org", "service_account_email", "authorization_code", "redirect_url")
    ORG_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_CODE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URL_FIELD_NUMBER: _ClassVar[int]
    org: str
    service_account_email: str
    authorization_code: str
    redirect_url: str
    def __init__(self, org: _Optional[str] = ..., service_account_email: _Optional[str] = ..., authorization_code: _Optional[str] = ..., redirect_url: _Optional[str] = ...) -> None: ...

class AuthorizeGcpCloudAccountCommandResponse(_message.Message):
    __slots__ = ("granted_roles",)
    GRANTED_ROLES_FIELD_NUMBER: _ClassVar[int]
    granted_roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, granted_roles: _Optional[_Iterable[str]] = ...) -> None: ...
