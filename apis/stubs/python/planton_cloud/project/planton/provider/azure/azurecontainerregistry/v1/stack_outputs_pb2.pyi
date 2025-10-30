from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AzureContainerRegistryStackOutputs(_message.Message):
    __slots__ = ("registry_login_server", "registry_resource_id")
    REGISTRY_LOGIN_SERVER_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    registry_login_server: str
    registry_resource_id: str
    def __init__(self, registry_login_server: _Optional[str] = ..., registry_resource_id: _Optional[str] = ...) -> None: ...
