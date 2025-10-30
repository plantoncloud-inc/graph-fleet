from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConfluentKafkaSpec(_message.Message):
    __slots__ = ("cloud", "availability", "environment")
    CLOUD_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    cloud: str
    availability: str
    environment: str
    def __init__(self, cloud: _Optional[str] = ..., availability: _Optional[str] = ..., environment: _Optional[str] = ...) -> None: ...
