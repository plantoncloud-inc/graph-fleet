from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_MASTER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_master_container: _descriptor.FieldDescriptor
DEFAULT_WORKER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_worker_container: _descriptor.FieldDescriptor

class LocustKubernetesSpec(_message.Message):
    __slots__ = ("master_container", "worker_container", "ingress", "load_test", "helm_values")
    class HelmValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    MASTER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    WORKER_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    LOAD_TEST_FIELD_NUMBER: _ClassVar[int]
    HELM_VALUES_FIELD_NUMBER: _ClassVar[int]
    master_container: LocustKubernetesContainer
    worker_container: LocustKubernetesContainer
    ingress: _kubernetes_pb2.IngressSpec
    load_test: LocustKubernetesLoadTest
    helm_values: _containers.ScalarMap[str, str]
    def __init__(self, master_container: _Optional[_Union[LocustKubernetesContainer, _Mapping]] = ..., worker_container: _Optional[_Union[LocustKubernetesContainer, _Mapping]] = ..., ingress: _Optional[_Union[_kubernetes_pb2.IngressSpec, _Mapping]] = ..., load_test: _Optional[_Union[LocustKubernetesLoadTest, _Mapping]] = ..., helm_values: _Optional[_Mapping[str, str]] = ...) -> None: ...

class LocustKubernetesContainer(_message.Message):
    __slots__ = ("replicas", "resources")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ...) -> None: ...

class LocustKubernetesLoadTest(_message.Message):
    __slots__ = ("name", "main_py_content", "lib_files_content", "pip_packages")
    class LibFilesContentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    MAIN_PY_CONTENT_FIELD_NUMBER: _ClassVar[int]
    LIB_FILES_CONTENT_FIELD_NUMBER: _ClassVar[int]
    PIP_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    name: str
    main_py_content: str
    lib_files_content: _containers.ScalarMap[str, str]
    pip_packages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., main_py_content: _Optional[str] = ..., lib_files_content: _Optional[_Mapping[str, str]] = ..., pip_packages: _Optional[_Iterable[str]] = ...) -> None: ...
