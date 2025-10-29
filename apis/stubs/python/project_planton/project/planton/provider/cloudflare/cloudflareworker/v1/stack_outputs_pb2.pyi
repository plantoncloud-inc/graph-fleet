from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareWorkerStackOutputs(_message.Message):
    __slots__ = ("script_id", "route_urls")
    SCRIPT_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTE_URLS_FIELD_NUMBER: _ClassVar[int]
    script_id: str
    route_urls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, script_id: _Optional[str] = ..., route_urls: _Optional[_Iterable[str]] = ...) -> None: ...
