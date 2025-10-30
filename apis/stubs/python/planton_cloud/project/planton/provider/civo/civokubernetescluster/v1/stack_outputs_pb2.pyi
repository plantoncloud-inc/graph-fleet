from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoKubernetesClusterStackOutputs(_message.Message):
    __slots__ = ("cluster_id", "kubeconfig_b64", "api_server_endpoint", "created_at_rfc3339")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    KUBECONFIG_B64_FIELD_NUMBER: _ClassVar[int]
    API_SERVER_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_RFC3339_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    kubeconfig_b64: str
    api_server_endpoint: str
    created_at_rfc3339: str
    def __init__(self, cluster_id: _Optional[str] = ..., kubeconfig_b64: _Optional[str] = ..., api_server_endpoint: _Optional[str] = ..., created_at_rfc3339: _Optional[str] = ...) -> None: ...
