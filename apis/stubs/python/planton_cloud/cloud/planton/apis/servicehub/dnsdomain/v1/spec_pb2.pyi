from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DnsDomainSpec(_message.Message):
    __slots__ = ("domain_name", "description")
    DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    domain_name: str
    description: str
    def __init__(self, domain_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
