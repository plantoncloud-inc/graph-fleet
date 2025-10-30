from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Neo4jKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "service", "bolt_uri_kube_endpoint", "http_uri_kube_endpoint")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    BOLT_URI_KUBE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    HTTP_URI_KUBE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    service: str
    bolt_uri_kube_endpoint: str
    http_uri_kube_endpoint: str
    def __init__(self, namespace: _Optional[str] = ..., service: _Optional[str] = ..., bolt_uri_kube_endpoint: _Optional[str] = ..., http_uri_kube_endpoint: _Optional[str] = ...) -> None: ...
