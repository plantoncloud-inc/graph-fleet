from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGkeClusterCoreStackOutputs(_message.Message):
    __slots__ = ("endpoint", "cluster_ca_certificate", "workload_identity_pool")
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CA_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_IDENTITY_POOL_FIELD_NUMBER: _ClassVar[int]
    endpoint: str
    cluster_ca_certificate: str
    workload_identity_pool: str
    def __init__(self, endpoint: _Optional[str] = ..., cluster_ca_certificate: _Optional[str] = ..., workload_identity_pool: _Optional[str] = ...) -> None: ...
