from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsStaticWebsiteStackOutputs(_message.Message):
    __slots__ = ("bucket_id",)
    BUCKET_ID_FIELD_NUMBER: _ClassVar[int]
    bucket_id: str
    def __init__(self, bucket_id: _Optional[str] = ...) -> None: ...
