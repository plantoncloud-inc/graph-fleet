from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanBucketStackOutputs(_message.Message):
    __slots__ = ("bucket_id", "endpoint")
    BUCKET_ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    bucket_id: str
    endpoint: str
    def __init__(self, bucket_id: _Optional[str] = ..., endpoint: _Optional[str] = ...) -> None: ...
