from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from project.planton.shared.options import options_pb2 as _options_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_BROKER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_broker_container: _descriptor.FieldDescriptor
DEFAULT_ZOOKEEPER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_zookeeper_container: _descriptor.FieldDescriptor

class KafkaKubernetesSpec(_message.Message):
    __slots__ = ("kafka_topics", "broker_container", "zookeeper_container", "schema_registry_container", "ingress", "is_deploy_kafka_ui")
    KAFKA_TOPICS_FIELD_NUMBER: _ClassVar[int]
    BROKER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    ZOOKEEPER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_REGISTRY_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    IS_DEPLOY_KAFKA_UI_FIELD_NUMBER: _ClassVar[int]
    kafka_topics: _containers.RepeatedCompositeFieldContainer[KafkaTopic]
    broker_container: KafkaKubernetesBrokerContainer
    zookeeper_container: KafkaKubernetesZookeeperContainer
    schema_registry_container: KafkaKubernetesSchemaRegistryContainer
    ingress: _kubernetes_pb2.IngressSpec
    is_deploy_kafka_ui: bool
    def __init__(self, kafka_topics: _Optional[_Iterable[_Union[KafkaTopic, _Mapping]]] = ..., broker_container: _Optional[_Union[KafkaKubernetesBrokerContainer, _Mapping]] = ..., zookeeper_container: _Optional[_Union[KafkaKubernetesZookeeperContainer, _Mapping]] = ..., schema_registry_container: _Optional[_Union[KafkaKubernetesSchemaRegistryContainer, _Mapping]] = ..., ingress: _Optional[_Union[_kubernetes_pb2.IngressSpec, _Mapping]] = ..., is_deploy_kafka_ui: bool = ...) -> None: ...

class KafkaKubernetesBrokerContainer(_message.Message):
    __slots__ = ("replicas", "resources", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., disk_size: _Optional[str] = ...) -> None: ...

class KafkaKubernetesZookeeperContainer(_message.Message):
    __slots__ = ("replicas", "resources", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., disk_size: _Optional[str] = ...) -> None: ...

class KafkaKubernetesSchemaRegistryContainer(_message.Message):
    __slots__ = ("is_enabled", "replicas", "resources")
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    is_enabled: bool
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    def __init__(self, is_enabled: bool = ..., replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ...) -> None: ...

class KafkaTopic(_message.Message):
    __slots__ = ("name", "partitions", "replicas", "config")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    partitions: int
    replicas: int
    config: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., partitions: _Optional[int] = ..., replicas: _Optional[int] = ..., config: _Optional[_Mapping[str, str]] = ...) -> None: ...
