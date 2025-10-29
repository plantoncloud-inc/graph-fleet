from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanDnsZoneStackOutputs(_message.Message):
    __slots__ = ("zone_name", "zone_id", "name_servers")
    ZONE_NAME_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_SERVERS_FIELD_NUMBER: _ClassVar[int]
    zone_name: str
    zone_id: str
    name_servers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, zone_name: _Optional[str] = ..., zone_id: _Optional[str] = ..., name_servers: _Optional[_Iterable[str]] = ...) -> None: ...
