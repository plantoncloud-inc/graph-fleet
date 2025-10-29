from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareDnsZoneStackOutputs(_message.Message):
    __slots__ = ("zone_id", "nameservers")
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESERVERS_FIELD_NUMBER: _ClassVar[int]
    zone_id: str
    nameservers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, zone_id: _Optional[str] = ..., nameservers: _Optional[_Iterable[str]] = ...) -> None: ...
