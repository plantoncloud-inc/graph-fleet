from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpVpcStackOutputs(_message.Message):
    __slots__ = ("network_self_link",)
    NETWORK_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    network_self_link: str
    def __init__(self, network_self_link: _Optional[str] = ...) -> None: ...
