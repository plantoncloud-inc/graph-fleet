from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NatsKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "client_url_internal", "client_url_external", "auth_token_secret", "jet_stream_domain", "metrics_endpoint", "tls_secret")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_URL_INTERNAL_FIELD_NUMBER: _ClassVar[int]
    CLIENT_URL_EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_SECRET_FIELD_NUMBER: _ClassVar[int]
    JET_STREAM_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    METRICS_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    TLS_SECRET_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    client_url_internal: str
    client_url_external: str
    auth_token_secret: _kubernetes_pb2.KubernetesSecretKey
    jet_stream_domain: str
    metrics_endpoint: str
    tls_secret: _kubernetes_pb2.KubernetesSecretKey
    def __init__(self, namespace: _Optional[str] = ..., client_url_internal: _Optional[str] = ..., client_url_external: _Optional[str] = ..., auth_token_secret: _Optional[_Union[_kubernetes_pb2.KubernetesSecretKey, _Mapping]] = ..., jet_stream_domain: _Optional[str] = ..., metrics_endpoint: _Optional[str] = ..., tls_secret: _Optional[_Union[_kubernetes_pb2.KubernetesSecretKey, _Mapping]] = ...) -> None: ...
