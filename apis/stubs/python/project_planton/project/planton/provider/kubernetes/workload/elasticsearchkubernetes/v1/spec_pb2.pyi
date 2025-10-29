from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_ELASTICSEARCH_SPEC_FIELD_NUMBER: _ClassVar[int]
default_elasticsearch_spec: _descriptor.FieldDescriptor
DEFAULT_KIBANA_SPEC_FIELD_NUMBER: _ClassVar[int]
default_kibana_spec: _descriptor.FieldDescriptor

class ElasticsearchKubernetesSpec(_message.Message):
    __slots__ = ("elasticsearch", "kibana")
    ELASTICSEARCH_FIELD_NUMBER: _ClassVar[int]
    KIBANA_FIELD_NUMBER: _ClassVar[int]
    elasticsearch: ElasticsearchKubernetesElasticsearchSpec
    kibana: ElasticsearchKubernetesKibanaSpec
    def __init__(self, elasticsearch: _Optional[_Union[ElasticsearchKubernetesElasticsearchSpec, _Mapping]] = ..., kibana: _Optional[_Union[ElasticsearchKubernetesKibanaSpec, _Mapping]] = ...) -> None: ...

class ElasticsearchKubernetesElasticsearchSpec(_message.Message):
    __slots__ = ("container", "ingress")
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    container: ElasticsearchKubernetesElasticsearchContainer
    ingress: ElasticsearchKubernetesIngress
    def __init__(self, container: _Optional[_Union[ElasticsearchKubernetesElasticsearchContainer, _Mapping]] = ..., ingress: _Optional[_Union[ElasticsearchKubernetesIngress, _Mapping]] = ...) -> None: ...

class ElasticsearchKubernetesKibanaSpec(_message.Message):
    __slots__ = ("enabled", "container", "ingress")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    container: ElasticsearchKubernetesKibanaContainer
    ingress: ElasticsearchKubernetesIngress
    def __init__(self, enabled: bool = ..., container: _Optional[_Union[ElasticsearchKubernetesKibanaContainer, _Mapping]] = ..., ingress: _Optional[_Union[ElasticsearchKubernetesIngress, _Mapping]] = ...) -> None: ...

class ElasticsearchKubernetesElasticsearchContainer(_message.Message):
    __slots__ = ("replicas", "resources", "persistence_enabled", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    persistence_enabled: bool
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., persistence_enabled: bool = ..., disk_size: _Optional[str] = ...) -> None: ...

class ElasticsearchKubernetesKibanaContainer(_message.Message):
    __slots__ = ("replicas", "resources")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ...) -> None: ...

class ElasticsearchKubernetesIngress(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...
