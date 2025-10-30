from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpCloudRunStackOutputs(_message.Message):
    __slots__ = ("url", "service_name", "revision")
    URL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    url: str
    service_name: str
    revision: str
    def __init__(self, url: _Optional[str] = ..., service_name: _Optional[str] = ..., revision: _Optional[str] = ...) -> None: ...
