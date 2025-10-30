from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanFunctionStackOutputs(_message.Message):
    __slots__ = ("function_id", "https_endpoint")
    FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    HTTPS_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    function_id: str
    https_endpoint: str
    def __init__(self, function_id: _Optional[str] = ..., https_endpoint: _Optional[str] = ...) -> None: ...
