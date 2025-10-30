from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareKvNamespaceStackOutputs(_message.Message):
    __slots__ = ("namespace_id",)
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    namespace_id: str
    def __init__(self, namespace_id: _Optional[str] = ...) -> None: ...
