from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanKubernetesNodePoolStackOutputs(_message.Message):
    __slots__ = ("node_pool_id", "node_ids")
    NODE_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_IDS_FIELD_NUMBER: _ClassVar[int]
    node_pool_id: str
    node_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, node_pool_id: _Optional[str] = ..., node_ids: _Optional[_Iterable[str]] = ...) -> None: ...
