from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KafkaKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "username", "password_secret", "bootstrap_server_external_hostname", "bootstrap_server_internal_hostname", "schema_registry_external_url", "schema_registry_internal_url", "kafka_ui_external_url")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_SECRET_FIELD_NUMBER: _ClassVar[int]
    BOOTSTRAP_SERVER_EXTERNAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    BOOTSTRAP_SERVER_INTERNAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_REGISTRY_EXTERNAL_URL_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_REGISTRY_INTERNAL_URL_FIELD_NUMBER: _ClassVar[int]
    KAFKA_UI_EXTERNAL_URL_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    username: str
    password_secret: _kubernetes_pb2.KubernetesSecretKey
    bootstrap_server_external_hostname: str
    bootstrap_server_internal_hostname: str
    schema_registry_external_url: str
    schema_registry_internal_url: str
    kafka_ui_external_url: str
    def __init__(self, namespace: _Optional[str] = ..., username: _Optional[str] = ..., password_secret: _Optional[_Union[_kubernetes_pb2.KubernetesSecretKey, _Mapping]] = ..., bootstrap_server_external_hostname: _Optional[str] = ..., bootstrap_server_internal_hostname: _Optional[str] = ..., schema_registry_external_url: _Optional[str] = ..., schema_registry_internal_url: _Optional[str] = ..., kafka_ui_external_url: _Optional[str] = ...) -> None: ...
