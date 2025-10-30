from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_SOLR_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_solr_container: _descriptor.FieldDescriptor
DEFAULT_ZOOKEEPER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_zookeeper_container: _descriptor.FieldDescriptor

class SolrKubernetesSpec(_message.Message):
    __slots__ = ("solr_container", "config", "zookeeper_container", "ingress")
    SOLR_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ZOOKEEPER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    solr_container: SolrKubernetesSolrContainer
    config: SolrKubernetesSolrConfig
    zookeeper_container: SolrKubernetesZookeeperContainer
    ingress: _kubernetes_pb2.IngressSpec
    def __init__(self, solr_container: _Optional[_Union[SolrKubernetesSolrContainer, _Mapping]] = ..., config: _Optional[_Union[SolrKubernetesSolrConfig, _Mapping]] = ..., zookeeper_container: _Optional[_Union[SolrKubernetesZookeeperContainer, _Mapping]] = ..., ingress: _Optional[_Union[_kubernetes_pb2.IngressSpec, _Mapping]] = ...) -> None: ...

class SolrKubernetesSolrContainer(_message.Message):
    __slots__ = ("replicas", "resources", "disk_size", "image")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    disk_size: str
    image: _kubernetes_pb2.ContainerImage
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., disk_size: _Optional[str] = ..., image: _Optional[_Union[_kubernetes_pb2.ContainerImage, _Mapping]] = ...) -> None: ...

class SolrKubernetesSolrConfig(_message.Message):
    __slots__ = ("java_mem", "opts", "garbage_collection_tuning")
    JAVA_MEM_FIELD_NUMBER: _ClassVar[int]
    OPTS_FIELD_NUMBER: _ClassVar[int]
    GARBAGE_COLLECTION_TUNING_FIELD_NUMBER: _ClassVar[int]
    java_mem: str
    opts: str
    garbage_collection_tuning: str
    def __init__(self, java_mem: _Optional[str] = ..., opts: _Optional[str] = ..., garbage_collection_tuning: _Optional[str] = ...) -> None: ...

class SolrKubernetesZookeeperContainer(_message.Message):
    __slots__ = ("replicas", "resources", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., disk_size: _Optional[str] = ...) -> None: ...
