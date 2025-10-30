from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AzureVpcStackOutputs(_message.Message):
    __slots__ = ("vnet_id", "nodes_subnet_id")
    VNET_ID_FIELD_NUMBER: _ClassVar[int]
    NODES_SUBNET_ID_FIELD_NUMBER: _ClassVar[int]
    vnet_id: str
    nodes_subnet_id: str
    def __init__(self, vnet_id: _Optional[str] = ..., nodes_subnet_id: _Optional[str] = ...) -> None: ...
