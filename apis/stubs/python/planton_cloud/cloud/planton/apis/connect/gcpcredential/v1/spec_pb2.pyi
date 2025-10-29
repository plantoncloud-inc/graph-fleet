from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpCredentialSpec(_message.Message):
    __slots__ = ("service_account_key_base64",)
    SERVICE_ACCOUNT_KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    service_account_key_base64: str
    def __init__(self, service_account_key_base64: _Optional[str] = ...) -> None: ...
