from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.integration.kubernetes.kubernetesobject import io_pb2 as _io_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceKubernetesObject(_message.Message):
    __slots__ = ("cloud_resource_id", "kubernetes_object")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_OBJECT_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    kubernetes_object: _io_pb2.KubernetesObject
    def __init__(self, cloud_resource_id: _Optional[str] = ..., kubernetes_object: _Optional[_Union[_io_pb2.KubernetesObject, _Mapping]] = ...) -> None: ...

class StreamKubernetesObjectsInNamespaceInput(_message.Message):
    __slots__ = ("cloud_resource_id", "namespace")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    namespace: str
    def __init__(self, cloud_resource_id: _Optional[str] = ..., namespace: _Optional[str] = ...) -> None: ...

class FindByKubernetesResourceKindInput(_message.Message):
    __slots__ = ("cloud_resource_id", "namespace", "kind")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    namespace: str
    kind: str
    def __init__(self, cloud_resource_id: _Optional[str] = ..., namespace: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...

class UpdateKubernetesObjectInput(_message.Message):
    __slots__ = ("cloud_resource_id", "kubernetes_object", "updated_object_yaml_base64")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_OBJECT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_OBJECT_YAML_BASE64_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    kubernetes_object: _io_pb2.KubernetesObject
    updated_object_yaml_base64: str
    def __init__(self, cloud_resource_id: _Optional[str] = ..., kubernetes_object: _Optional[_Union[_io_pb2.KubernetesObject, _Mapping]] = ..., updated_object_yaml_base64: _Optional[str] = ...) -> None: ...

class FindKubernetesPodsInput(_message.Message):
    __slots__ = ("cloud_resource_id", "namespace", "pod_manager")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_MANAGER_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    namespace: str
    pod_manager: _io_pb2.KubernetesObject
    def __init__(self, cloud_resource_id: _Optional[str] = ..., namespace: _Optional[str] = ..., pod_manager: _Optional[_Union[_io_pb2.KubernetesObject, _Mapping]] = ...) -> None: ...

class LookupCloudResourceKubernetesSecretKeyValueInput(_message.Message):
    __slots__ = ("cloud_resource_id", "kubernetes_secret_key")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_SECRET_KEY_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    kubernetes_secret_key: _kubernetes_pb2.KubernetesSecretKey
    def __init__(self, cloud_resource_id: _Optional[str] = ..., kubernetes_secret_key: _Optional[_Union[_kubernetes_pb2.KubernetesSecretKey, _Mapping]] = ...) -> None: ...

class KubernetesSecretKeyValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...
