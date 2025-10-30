from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsCloudFrontStackOutputs(_message.Message):
    __slots__ = ("distribution_id", "domain_name", "hosted_zone_id")
    DISTRIBUTION_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    HOSTED_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    distribution_id: str
    domain_name: str
    hosted_zone_id: str
    def __init__(self, distribution_id: _Optional[str] = ..., domain_name: _Optional[str] = ..., hosted_zone_id: _Optional[str] = ...) -> None: ...
