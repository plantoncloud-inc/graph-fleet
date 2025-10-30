from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesHttpEndpointSpec(_message.Message):
    __slots__ = ("is_tls_enabled", "cert_cluster_issuer_name", "is_grpc_web_compatible", "routing_rules")
    IS_TLS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CERT_CLUSTER_ISSUER_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_GRPC_WEB_COMPATIBLE_FIELD_NUMBER: _ClassVar[int]
    ROUTING_RULES_FIELD_NUMBER: _ClassVar[int]
    is_tls_enabled: bool
    cert_cluster_issuer_name: str
    is_grpc_web_compatible: bool
    routing_rules: _containers.RepeatedCompositeFieldContainer[KubernetesHttpEndpointRoutingRule]
    def __init__(self, is_tls_enabled: bool = ..., cert_cluster_issuer_name: _Optional[str] = ..., is_grpc_web_compatible: bool = ..., routing_rules: _Optional[_Iterable[_Union[KubernetesHttpEndpointRoutingRule, _Mapping]]] = ...) -> None: ...

class KubernetesHttpEndpointRoutingRule(_message.Message):
    __slots__ = ("url_path_prefix", "backend_service")
    URL_PATH_PREFIX_FIELD_NUMBER: _ClassVar[int]
    BACKEND_SERVICE_FIELD_NUMBER: _ClassVar[int]
    url_path_prefix: str
    backend_service: KubernetesHttpEndpointRoutingRuleBackendService
    def __init__(self, url_path_prefix: _Optional[str] = ..., backend_service: _Optional[_Union[KubernetesHttpEndpointRoutingRuleBackendService, _Mapping]] = ...) -> None: ...

class KubernetesHttpEndpointRoutingRuleBackendService(_message.Message):
    __slots__ = ("name", "namespace", "port")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    port: int
    def __init__(self, name: _Optional[str] = ..., namespace: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...
