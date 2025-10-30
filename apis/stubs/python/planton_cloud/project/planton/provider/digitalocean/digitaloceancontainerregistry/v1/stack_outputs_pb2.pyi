from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanContainerRegistryStackOutputs(_message.Message):
    __slots__ = ("registry_name", "server_url", "region")
    REGISTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_URL_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    registry_name: str
    server_url: str
    region: str
    def __init__(self, registry_name: _Optional[str] = ..., server_url: _Optional[str] = ..., region: _Optional[str] = ...) -> None: ...
