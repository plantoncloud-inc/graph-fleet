from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SignozKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "signoz_service", "otel_collector_service", "port_forward_command", "kube_endpoint", "external_hostname", "internal_hostname", "otel_collector_grpc_endpoint", "otel_collector_http_endpoint", "otel_collector_external_grpc_hostname", "otel_collector_external_http_hostname", "clickhouse_endpoint", "clickhouse_username", "clickhouse_password_secret")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SIGNOZ_SERVICE_FIELD_NUMBER: _ClassVar[int]
    OTEL_COLLECTOR_SERVICE_FIELD_NUMBER: _ClassVar[int]
    PORT_FORWARD_COMMAND_FIELD_NUMBER: _ClassVar[int]
    KUBE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    OTEL_COLLECTOR_GRPC_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    OTEL_COLLECTOR_HTTP_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    OTEL_COLLECTOR_EXTERNAL_GRPC_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    OTEL_COLLECTOR_EXTERNAL_HTTP_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    CLICKHOUSE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    CLICKHOUSE_USERNAME_FIELD_NUMBER: _ClassVar[int]
    CLICKHOUSE_PASSWORD_SECRET_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    signoz_service: str
    otel_collector_service: str
    port_forward_command: str
    kube_endpoint: str
    external_hostname: str
    internal_hostname: str
    otel_collector_grpc_endpoint: str
    otel_collector_http_endpoint: str
    otel_collector_external_grpc_hostname: str
    otel_collector_external_http_hostname: str
    clickhouse_endpoint: str
    clickhouse_username: str
    clickhouse_password_secret: _kubernetes_pb2.KubernetesSecretKey
    def __init__(self, namespace: _Optional[str] = ..., signoz_service: _Optional[str] = ..., otel_collector_service: _Optional[str] = ..., port_forward_command: _Optional[str] = ..., kube_endpoint: _Optional[str] = ..., external_hostname: _Optional[str] = ..., internal_hostname: _Optional[str] = ..., otel_collector_grpc_endpoint: _Optional[str] = ..., otel_collector_http_endpoint: _Optional[str] = ..., otel_collector_external_grpc_hostname: _Optional[str] = ..., otel_collector_external_http_hostname: _Optional[str] = ..., clickhouse_endpoint: _Optional[str] = ..., clickhouse_username: _Optional[str] = ..., clickhouse_password_secret: _Optional[_Union[_kubernetes_pb2.KubernetesSecretKey, _Mapping]] = ...) -> None: ...
