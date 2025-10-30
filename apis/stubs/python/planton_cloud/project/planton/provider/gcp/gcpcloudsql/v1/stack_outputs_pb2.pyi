from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpCloudSqlStackOutputs(_message.Message):
    __slots__ = ("lambda_function_id",)
    LAMBDA_FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    lambda_function_id: str
    def __init__(self, lambda_function_id: _Optional[str] = ...) -> None: ...
