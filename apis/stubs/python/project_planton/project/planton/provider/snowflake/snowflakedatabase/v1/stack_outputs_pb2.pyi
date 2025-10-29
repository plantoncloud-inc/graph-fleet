from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SnowflakeDatabaseStackOutputs(_message.Message):
    __slots__ = ("id", "bootstrap_endpoint", "crn", "rest_endpoint")
    ID_FIELD_NUMBER: _ClassVar[int]
    BOOTSTRAP_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    CRN_FIELD_NUMBER: _ClassVar[int]
    REST_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    id: str
    bootstrap_endpoint: str
    crn: str
    rest_endpoint: str
    def __init__(self, id: _Optional[str] = ..., bootstrap_endpoint: _Optional[str] = ..., crn: _Optional[str] = ..., rest_endpoint: _Optional[str] = ...) -> None: ...
