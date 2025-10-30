from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanKubernetesClusterStackOutputs(_message.Message):
    __slots__ = ("cluster_id", "kubeconfig", "api_server_endpoint")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    KUBECONFIG_FIELD_NUMBER: _ClassVar[int]
    API_SERVER_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    kubeconfig: str
    api_server_endpoint: str
    def __init__(self, cluster_id: _Optional[str] = ..., kubeconfig: _Optional[str] = ..., api_server_endpoint: _Optional[str] = ...) -> None: ...
