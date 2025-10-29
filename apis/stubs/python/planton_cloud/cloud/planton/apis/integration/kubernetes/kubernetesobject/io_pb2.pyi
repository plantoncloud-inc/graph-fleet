from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesObject(_message.Message):
    __slots__ = ("is_system_object", "namespace", "api_version", "kind", "name", "is_pod_manager")
    IS_SYSTEM_OBJECT_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_POD_MANAGER_FIELD_NUMBER: _ClassVar[int]
    is_system_object: bool
    namespace: str
    api_version: str
    kind: str
    name: str
    is_pod_manager: bool
    def __init__(self, is_system_object: bool = ..., namespace: _Optional[str] = ..., api_version: _Optional[str] = ..., kind: _Optional[str] = ..., name: _Optional[str] = ..., is_pod_manager: bool = ...) -> None: ...

class KubernetesObjectList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[KubernetesObject]
    def __init__(self, entries: _Optional[_Iterable[_Union[KubernetesObject, _Mapping]]] = ...) -> None: ...

class KubernetesPod(_message.Message):
    __slots__ = ("pod_manager", "namespace", "name", "labels", "status", "status_reason", "status_message", "containers", "containers_in_ready_state", "containers_restart_count")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    POD_MANAGER_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_REASON_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    CONTAINERS_IN_READY_STATE_FIELD_NUMBER: _ClassVar[int]
    CONTAINERS_RESTART_COUNT_FIELD_NUMBER: _ClassVar[int]
    pod_manager: KubernetesObject
    namespace: str
    name: str
    labels: _containers.ScalarMap[str, str]
    status: str
    status_reason: str
    status_message: str
    containers: _containers.RepeatedCompositeFieldContainer[KubernetesPodContainer]
    containers_in_ready_state: str
    containers_restart_count: int
    def __init__(self, pod_manager: _Optional[_Union[KubernetesObject, _Mapping]] = ..., namespace: _Optional[str] = ..., name: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ..., status: _Optional[str] = ..., status_reason: _Optional[str] = ..., status_message: _Optional[str] = ..., containers: _Optional[_Iterable[_Union[KubernetesPodContainer, _Mapping]]] = ..., containers_in_ready_state: _Optional[str] = ..., containers_restart_count: _Optional[int] = ...) -> None: ...

class KubernetesPodContainer(_message.Message):
    __slots__ = ("name", "image", "status", "status_reason", "status_message", "restart_count")
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_REASON_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESTART_COUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    image: str
    status: str
    status_reason: str
    status_message: str
    restart_count: int
    def __init__(self, name: _Optional[str] = ..., image: _Optional[str] = ..., status: _Optional[str] = ..., status_reason: _Optional[str] = ..., status_message: _Optional[str] = ..., restart_count: _Optional[int] = ...) -> None: ...

class KubernetesPodList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[KubernetesPod]
    def __init__(self, entries: _Optional[_Iterable[_Union[KubernetesPod, _Mapping]]] = ...) -> None: ...

class StreamKubernetesObjectsInNamespaceWithKubeConfigInput(_message.Message):
    __slots__ = ("kube_config_base64", "namespace")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    namespace: str
    def __init__(self, kube_config_base64: _Optional[str] = ..., namespace: _Optional[str] = ...) -> None: ...

class KubernetesObjectDetail(_message.Message):
    __slots__ = ("kubernetes_object", "describe_format_base64", "yaml_format_base64")
    KUBERNETES_OBJECT_FIELD_NUMBER: _ClassVar[int]
    DESCRIBE_FORMAT_BASE64_FIELD_NUMBER: _ClassVar[int]
    YAML_FORMAT_BASE64_FIELD_NUMBER: _ClassVar[int]
    kubernetes_object: KubernetesObject
    describe_format_base64: str
    yaml_format_base64: str
    def __init__(self, kubernetes_object: _Optional[_Union[KubernetesObject, _Mapping]] = ..., describe_format_base64: _Optional[str] = ..., yaml_format_base64: _Optional[str] = ...) -> None: ...

class GetKubernetesObjectWithKubeConfigInput(_message.Message):
    __slots__ = ("kube_config_base64", "kubernetes_object")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_OBJECT_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    kubernetes_object: KubernetesObject
    def __init__(self, kube_config_base64: _Optional[str] = ..., kubernetes_object: _Optional[_Union[KubernetesObject, _Mapping]] = ...) -> None: ...

class FindPodsWithKubeConfigInput(_message.Message):
    __slots__ = ("kube_config_base64", "namespace", "pod_manager")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_MANAGER_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    namespace: str
    pod_manager: KubernetesObject
    def __init__(self, kube_config_base64: _Optional[str] = ..., namespace: _Optional[str] = ..., pod_manager: _Optional[_Union[KubernetesObject, _Mapping]] = ...) -> None: ...

class StreamPodLogsWithKubeConfigInput(_message.Message):
    __slots__ = ("kube_config_base64", "options")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    options: PodLogStreamOptions
    def __init__(self, kube_config_base64: _Optional[str] = ..., options: _Optional[_Union[PodLogStreamOptions, _Mapping]] = ...) -> None: ...

class PodLogStreamOptions(_message.Message):
    __slots__ = ("namespace", "pod_manager", "pod_name_filter", "container_name_filter", "is_fetch_previous_container_logs", "since_duration", "tail_lines", "content_filter")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_MANAGER_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_FILTER_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FILTER_FIELD_NUMBER: _ClassVar[int]
    IS_FETCH_PREVIOUS_CONTAINER_LOGS_FIELD_NUMBER: _ClassVar[int]
    SINCE_DURATION_FIELD_NUMBER: _ClassVar[int]
    TAIL_LINES_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FILTER_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pod_manager: KubernetesObject
    pod_name_filter: str
    container_name_filter: str
    is_fetch_previous_container_logs: bool
    since_duration: str
    tail_lines: int
    content_filter: str
    def __init__(self, namespace: _Optional[str] = ..., pod_manager: _Optional[_Union[KubernetesObject, _Mapping]] = ..., pod_name_filter: _Optional[str] = ..., container_name_filter: _Optional[str] = ..., is_fetch_previous_container_logs: bool = ..., since_duration: _Optional[str] = ..., tail_lines: _Optional[int] = ..., content_filter: _Optional[str] = ...) -> None: ...

class PodLogLine(_message.Message):
    __slots__ = ("pod_name", "container_name", "log_line")
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    LOG_LINE_FIELD_NUMBER: _ClassVar[int]
    pod_name: str
    container_name: str
    log_line: str
    def __init__(self, pod_name: _Optional[str] = ..., container_name: _Optional[str] = ..., log_line: _Optional[str] = ...) -> None: ...

class DeleteKubernetesObjectWithKubeConfigInput(_message.Message):
    __slots__ = ("kube_config_base64", "kubernetes_object")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_OBJECT_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    kubernetes_object: KubernetesObject
    def __init__(self, kube_config_base64: _Optional[str] = ..., kubernetes_object: _Optional[_Union[KubernetesObject, _Mapping]] = ...) -> None: ...

class UpdateKubernetesObjectWithKubeConfigInput(_message.Message):
    __slots__ = ("kube_config_base64", "kubernetes_object", "updated_object_yaml_base64")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_OBJECT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_OBJECT_YAML_BASE64_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    kubernetes_object: KubernetesObject
    updated_object_yaml_base64: str
    def __init__(self, kube_config_base64: _Optional[str] = ..., kubernetes_object: _Optional[_Union[KubernetesObject, _Mapping]] = ..., updated_object_yaml_base64: _Optional[str] = ...) -> None: ...

class PodContainerExecOptions(_message.Message):
    __slots__ = ("pod", "container_name", "shell", "command")
    POD_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    SHELL_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    pod: KubernetesObject
    container_name: str
    shell: str
    command: str
    def __init__(self, pod: _Optional[_Union[KubernetesObject, _Mapping]] = ..., container_name: _Optional[str] = ..., shell: _Optional[str] = ..., command: _Optional[str] = ...) -> None: ...

class ExecIntoPodContainerWithKubeConfigInput(_message.Message):
    __slots__ = ("kube_config_base64", "options")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    options: PodContainerExecOptions
    def __init__(self, kube_config_base64: _Optional[str] = ..., options: _Optional[_Union[PodContainerExecOptions, _Mapping]] = ...) -> None: ...

class ExecIntoPodContainerResponse(_message.Message):
    __slots__ = ("stdout", "stderr")
    STDOUT_FIELD_NUMBER: _ClassVar[int]
    STDERR_FIELD_NUMBER: _ClassVar[int]
    stdout: str
    stderr: str
    def __init__(self, stdout: _Optional[str] = ..., stderr: _Optional[str] = ...) -> None: ...

class KubernetesNamespace(_message.Message):
    __slots__ = ("name", "status", "age")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: str
    age: str
    def __init__(self, name: _Optional[str] = ..., status: _Optional[str] = ..., age: _Optional[str] = ...) -> None: ...

class KubernetesNamespaceList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[KubernetesNamespace]
    def __init__(self, entries: _Optional[_Iterable[_Union[KubernetesNamespace, _Mapping]]] = ...) -> None: ...

class KubeConfigBase64Encoded(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class FindByKubernetesResourceKindWithKubeConfigInput(_message.Message):
    __slots__ = ("kube_config_base64", "namespace", "kind")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    namespace: str
    kind: str
    def __init__(self, kube_config_base64: _Optional[str] = ..., namespace: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...
