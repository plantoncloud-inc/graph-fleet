from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoCertificateStackOutputs(_message.Message):
    __slots__ = ("certificate_id", "expiry_rfc3339")
    CERTIFICATE_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_RFC3339_FIELD_NUMBER: _ClassVar[int]
    certificate_id: str
    expiry_rfc3339: str
    def __init__(self, certificate_id: _Optional[str] = ..., expiry_rfc3339: _Optional[str] = ...) -> None: ...
