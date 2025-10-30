from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TemporalKubernetesDatabaseBackend(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    temporal_kubernetes_database_backend_unspecified: _ClassVar[TemporalKubernetesDatabaseBackend]
    cassandra: _ClassVar[TemporalKubernetesDatabaseBackend]
    postgresql: _ClassVar[TemporalKubernetesDatabaseBackend]
    mysql: _ClassVar[TemporalKubernetesDatabaseBackend]
temporal_kubernetes_database_backend_unspecified: TemporalKubernetesDatabaseBackend
cassandra: TemporalKubernetesDatabaseBackend
postgresql: TemporalKubernetesDatabaseBackend
mysql: TemporalKubernetesDatabaseBackend

class TemporalKubernetesSpec(_message.Message):
    __slots__ = ("database", "disable_web_ui", "enable_embedded_elasticsearch", "enable_monitoring_stack", "cassandra_replicas", "ingress", "external_elasticsearch", "version")
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_WEB_UI_FIELD_NUMBER: _ClassVar[int]
    ENABLE_EMBEDDED_ELASTICSEARCH_FIELD_NUMBER: _ClassVar[int]
    ENABLE_MONITORING_STACK_FIELD_NUMBER: _ClassVar[int]
    CASSANDRA_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ELASTICSEARCH_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    database: TemporalKubernetesDatabaseConfig
    disable_web_ui: bool
    enable_embedded_elasticsearch: bool
    enable_monitoring_stack: bool
    cassandra_replicas: int
    ingress: TemporalKubernetesIngress
    external_elasticsearch: TemporalKubernetesExternalElasticsearch
    version: str
    def __init__(self, database: _Optional[_Union[TemporalKubernetesDatabaseConfig, _Mapping]] = ..., disable_web_ui: bool = ..., enable_embedded_elasticsearch: bool = ..., enable_monitoring_stack: bool = ..., cassandra_replicas: _Optional[int] = ..., ingress: _Optional[_Union[TemporalKubernetesIngress, _Mapping]] = ..., external_elasticsearch: _Optional[_Union[TemporalKubernetesExternalElasticsearch, _Mapping]] = ..., version: _Optional[str] = ...) -> None: ...

class TemporalKubernetesDatabaseConfig(_message.Message):
    __slots__ = ("backend", "external_database", "database_name", "visibility_name", "disable_auto_schema_setup")
    BACKEND_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_DATABASE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_NAME_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AUTO_SCHEMA_SETUP_FIELD_NUMBER: _ClassVar[int]
    backend: TemporalKubernetesDatabaseBackend
    external_database: TemporalKubernetesExternalDatabase
    database_name: str
    visibility_name: str
    disable_auto_schema_setup: bool
    def __init__(self, backend: _Optional[_Union[TemporalKubernetesDatabaseBackend, str]] = ..., external_database: _Optional[_Union[TemporalKubernetesExternalDatabase, _Mapping]] = ..., database_name: _Optional[str] = ..., visibility_name: _Optional[str] = ..., disable_auto_schema_setup: bool = ...) -> None: ...

class TemporalKubernetesExternalDatabase(_message.Message):
    __slots__ = ("host", "port", "username", "password")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    username: str
    password: str
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class TemporalKubernetesExternalElasticsearch(_message.Message):
    __slots__ = ("host", "port", "user", "password")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    user: str
    password: str
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., user: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class TemporalKubernetesIngress(_message.Message):
    __slots__ = ("frontend", "web_ui")
    FRONTEND_FIELD_NUMBER: _ClassVar[int]
    WEB_UI_FIELD_NUMBER: _ClassVar[int]
    frontend: TemporalKubernetesIngressEndpoint
    web_ui: TemporalKubernetesIngressEndpoint
    def __init__(self, frontend: _Optional[_Union[TemporalKubernetesIngressEndpoint, _Mapping]] = ..., web_ui: _Optional[_Union[TemporalKubernetesIngressEndpoint, _Mapping]] = ...) -> None: ...

class TemporalKubernetesIngressEndpoint(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...
