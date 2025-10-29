from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AzureAksClusterStackOutputs(_message.Message):
    __slots__ = ("api_server_endpoint", "cluster_resource_id", "cluster_kubeconfig", "managed_identity_principal_id")
    API_SERVER_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_KUBECONFIG_FIELD_NUMBER: _ClassVar[int]
    MANAGED_IDENTITY_PRINCIPAL_ID_FIELD_NUMBER: _ClassVar[int]
    api_server_endpoint: str
    cluster_resource_id: str
    cluster_kubeconfig: str
    managed_identity_principal_id: str
    def __init__(self, api_server_endpoint: _Optional[str] = ..., cluster_resource_id: _Optional[str] = ..., cluster_kubeconfig: _Optional[str] = ..., managed_identity_principal_id: _Optional[str] = ...) -> None: ...
