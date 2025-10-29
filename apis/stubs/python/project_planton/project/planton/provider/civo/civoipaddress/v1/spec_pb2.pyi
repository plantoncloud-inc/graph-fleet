from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.civo import region_pb2 as _region_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CivoIpAddressSpec(_message.Message):
    __slots__ = ("description", "region")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    description: str
    region: _region_pb2.CivoRegion
    def __init__(self, description: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.CivoRegion, str]] = ...) -> None: ...
