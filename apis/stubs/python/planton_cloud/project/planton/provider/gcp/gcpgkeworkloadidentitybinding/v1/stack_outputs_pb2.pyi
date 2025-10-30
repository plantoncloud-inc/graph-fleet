from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGkeWorkloadIdentityBindingStackOutputs(_message.Message):
    __slots__ = ("member", "service_account_email")
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    member: str
    service_account_email: str
    def __init__(self, member: _Optional[str] = ..., service_account_email: _Optional[str] = ...) -> None: ...
