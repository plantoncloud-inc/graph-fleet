from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareZeroTrustAccessApplicationStackOutputs(_message.Message):
    __slots__ = ("application_id", "public_hostname", "policy_id")
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    application_id: str
    public_hostname: str
    policy_id: str
    def __init__(self, application_id: _Optional[str] = ..., public_hostname: _Optional[str] = ..., policy_id: _Optional[str] = ...) -> None: ...
