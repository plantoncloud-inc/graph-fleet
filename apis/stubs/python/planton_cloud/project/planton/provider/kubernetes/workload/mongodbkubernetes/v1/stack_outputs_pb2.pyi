from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MongodbKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "service", "port_forward_command", "kube_endpoint", "external_hostname", "internal_hostname", "username", "password_secret")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    PORT_FORWARD_COMMAND_FIELD_NUMBER: _ClassVar[int]
    KUBE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_SECRET_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    service: str
    port_forward_command: str
    kube_endpoint: str
    external_hostname: str
    internal_hostname: str
    username: str
    password_secret: _kubernetes_pb2.KubernetesSecretKey
    def __init__(self, namespace: _Optional[str] = ..., service: _Optional[str] = ..., port_forward_command: _Optional[str] = ..., kube_endpoint: _Optional[str] = ..., external_hostname: _Optional[str] = ..., internal_hostname: _Optional[str] = ..., username: _Optional[str] = ..., password_secret: _Optional[_Union[_kubernetes_pb2.KubernetesSecretKey, _Mapping]] = ...) -> None: ...
