from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareR2BucketStackOutputs(_message.Message):
    __slots__ = ("bucket_name", "bucket_url")
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    BUCKET_URL_FIELD_NUMBER: _ClassVar[int]
    bucket_name: str
    bucket_url: str
    def __init__(self, bucket_name: _Optional[str] = ..., bucket_url: _Optional[str] = ...) -> None: ...
