from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsS3BucketSpec(_message.Message):
    __slots__ = ("is_public", "aws_region")
    IS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    AWS_REGION_FIELD_NUMBER: _ClassVar[int]
    is_public: bool
    aws_region: str
    def __init__(self, is_public: bool = ..., aws_region: _Optional[str] = ...) -> None: ...
