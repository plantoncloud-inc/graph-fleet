from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AzureAksNodePoolStackOutputs(_message.Message):
    __slots__ = ("node_pool_name", "agent_pool_resource_id", "max_pods_per_node")
    NODE_POOL_NAME_FIELD_NUMBER: _ClassVar[int]
    AGENT_POOL_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_PODS_PER_NODE_FIELD_NUMBER: _ClassVar[int]
    node_pool_name: str
    agent_pool_resource_id: str
    max_pods_per_node: int
    def __init__(self, node_pool_name: _Optional[str] = ..., agent_pool_resource_id: _Optional[str] = ..., max_pods_per_node: _Optional[int] = ...) -> None: ...
