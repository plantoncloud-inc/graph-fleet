from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ElasticOperatorKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "service", "port_forward_command", "kube_endpoint", "ingress_endpoint")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    PORT_FORWARD_COMMAND_FIELD_NUMBER: _ClassVar[int]
    KUBE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    INGRESS_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    service: str
    port_forward_command: str
    kube_endpoint: str
    ingress_endpoint: str
    def __init__(self, namespace: _Optional[str] = ..., service: _Optional[str] = ..., port_forward_command: _Optional[str] = ..., kube_endpoint: _Optional[str] = ..., ingress_endpoint: _Optional[str] = ...) -> None: ...
