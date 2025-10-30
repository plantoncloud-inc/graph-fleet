from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.kubernetes import probe_pb2 as _probe_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MicroserviceKubernetesSpec(_message.Message):
    __slots__ = ("version", "container", "ingress", "availability")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    version: str
    container: MicroserviceKubernetesContainer
    ingress: _kubernetes_pb2.IngressSpec
    availability: MicroserviceKubernetesAvailability
    def __init__(self, version: _Optional[str] = ..., container: _Optional[_Union[MicroserviceKubernetesContainer, _Mapping]] = ..., ingress: _Optional[_Union[_kubernetes_pb2.IngressSpec, _Mapping]] = ..., availability: _Optional[_Union[MicroserviceKubernetesAvailability, _Mapping]] = ...) -> None: ...

class MicroserviceKubernetesContainer(_message.Message):
    __slots__ = ("app", "sidecars")
    APP_FIELD_NUMBER: _ClassVar[int]
    SIDECARS_FIELD_NUMBER: _ClassVar[int]
    app: MicroserviceKubernetesContainerApp
    sidecars: _containers.RepeatedCompositeFieldContainer[_kubernetes_pb2.Container]
    def __init__(self, app: _Optional[_Union[MicroserviceKubernetesContainerApp, _Mapping]] = ..., sidecars: _Optional[_Iterable[_Union[_kubernetes_pb2.Container, _Mapping]]] = ...) -> None: ...

class MicroserviceKubernetesContainerApp(_message.Message):
    __slots__ = ("image", "resources", "env", "ports", "liveness_probe", "readiness_probe", "startup_probe")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    LIVENESS_PROBE_FIELD_NUMBER: _ClassVar[int]
    READINESS_PROBE_FIELD_NUMBER: _ClassVar[int]
    STARTUP_PROBE_FIELD_NUMBER: _ClassVar[int]
    image: _kubernetes_pb2.ContainerImage
    resources: _kubernetes_pb2.ContainerResources
    env: MicroserviceKubernetesContainerAppEnv
    ports: _containers.RepeatedCompositeFieldContainer[MicroserviceKubernetesContainerAppPort]
    liveness_probe: _probe_pb2.Probe
    readiness_probe: _probe_pb2.Probe
    startup_probe: _probe_pb2.Probe
    def __init__(self, image: _Optional[_Union[_kubernetes_pb2.ContainerImage, _Mapping]] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., env: _Optional[_Union[MicroserviceKubernetesContainerAppEnv, _Mapping]] = ..., ports: _Optional[_Iterable[_Union[MicroserviceKubernetesContainerAppPort, _Mapping]]] = ..., liveness_probe: _Optional[_Union[_probe_pb2.Probe, _Mapping]] = ..., readiness_probe: _Optional[_Union[_probe_pb2.Probe, _Mapping]] = ..., startup_probe: _Optional[_Union[_probe_pb2.Probe, _Mapping]] = ...) -> None: ...

class MicroserviceKubernetesContainerAppEnv(_message.Message):
    __slots__ = ("variables", "secrets")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SecretsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.ScalarMap[str, str]
    secrets: _containers.ScalarMap[str, str]
    def __init__(self, variables: _Optional[_Mapping[str, str]] = ..., secrets: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MicroserviceKubernetesContainerAppPort(_message.Message):
    __slots__ = ("name", "container_port", "network_protocol", "app_protocol", "service_port", "is_ingress_port")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_PORT_FIELD_NUMBER: _ClassVar[int]
    NETWORK_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    APP_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_PORT_FIELD_NUMBER: _ClassVar[int]
    IS_INGRESS_PORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    container_port: int
    network_protocol: str
    app_protocol: str
    service_port: int
    is_ingress_port: bool
    def __init__(self, name: _Optional[str] = ..., container_port: _Optional[int] = ..., network_protocol: _Optional[str] = ..., app_protocol: _Optional[str] = ..., service_port: _Optional[int] = ..., is_ingress_port: bool = ...) -> None: ...

class MicroserviceKubernetesAvailability(_message.Message):
    __slots__ = ("min_replicas", "horizontal_pod_autoscaling", "deployment_strategy", "pod_disruption_budget")
    MIN_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_POD_AUTOSCALING_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    POD_DISRUPTION_BUDGET_FIELD_NUMBER: _ClassVar[int]
    min_replicas: int
    horizontal_pod_autoscaling: MicroserviceKubernetesAvailabilityHpa
    deployment_strategy: MicroserviceKubernetesDeploymentStrategy
    pod_disruption_budget: MicroserviceKubernetesPodDisruptionBudget
    def __init__(self, min_replicas: _Optional[int] = ..., horizontal_pod_autoscaling: _Optional[_Union[MicroserviceKubernetesAvailabilityHpa, _Mapping]] = ..., deployment_strategy: _Optional[_Union[MicroserviceKubernetesDeploymentStrategy, _Mapping]] = ..., pod_disruption_budget: _Optional[_Union[MicroserviceKubernetesPodDisruptionBudget, _Mapping]] = ...) -> None: ...

class MicroserviceKubernetesAvailabilityHpa(_message.Message):
    __slots__ = ("is_enabled", "target_cpu_utilization_percent", "target_memory_utilization")
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TARGET_CPU_UTILIZATION_PERCENT_FIELD_NUMBER: _ClassVar[int]
    TARGET_MEMORY_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    is_enabled: bool
    target_cpu_utilization_percent: float
    target_memory_utilization: str
    def __init__(self, is_enabled: bool = ..., target_cpu_utilization_percent: _Optional[float] = ..., target_memory_utilization: _Optional[str] = ...) -> None: ...

class MicroserviceKubernetesDeploymentStrategy(_message.Message):
    __slots__ = ("max_unavailable", "max_surge")
    MAX_UNAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    MAX_SURGE_FIELD_NUMBER: _ClassVar[int]
    max_unavailable: str
    max_surge: str
    def __init__(self, max_unavailable: _Optional[str] = ..., max_surge: _Optional[str] = ...) -> None: ...

class MicroserviceKubernetesPodDisruptionBudget(_message.Message):
    __slots__ = ("enabled", "min_available", "max_unavailable")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MIN_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    MAX_UNAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    min_available: str
    max_unavailable: str
    def __init__(self, enabled: bool = ..., min_available: _Optional[str] = ..., max_unavailable: _Optional[str] = ...) -> None: ...
