from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesObjectKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    kubernetes_object_kind_unspecified: _ClassVar[KubernetesObjectKind]
    Deployment: _ClassVar[KubernetesObjectKind]
    Pod: _ClassVar[KubernetesObjectKind]
    Service: _ClassVar[KubernetesObjectKind]
    ClusterRole: _ClassVar[KubernetesObjectKind]
    ConfigMap: _ClassVar[KubernetesObjectKind]
    ClusterRoleBinding: _ClassVar[KubernetesObjectKind]
    CustomResourceDefinition: _ClassVar[KubernetesObjectKind]
    CronJob: _ClassVar[KubernetesObjectKind]
    DaemonSet: _ClassVar[KubernetesObjectKind]
    Endpoints: _ClassVar[KubernetesObjectKind]
    Group: _ClassVar[KubernetesObjectKind]
    HorizontalPodAutoscaler: _ClassVar[KubernetesObjectKind]
    Ingress: _ClassVar[KubernetesObjectKind]
    Job: _ClassVar[KubernetesObjectKind]
    LimitRange: _ClassVar[KubernetesObjectKind]
    NetworkPolicy: _ClassVar[KubernetesObjectKind]
    Namespace: _ClassVar[KubernetesObjectKind]
    PodSecurityPolicy: _ClassVar[KubernetesObjectKind]
    PersistentVolume: _ClassVar[KubernetesObjectKind]
    PersistentVolumeClaim: _ClassVar[KubernetesObjectKind]
    ResourceQuota: _ClassVar[KubernetesObjectKind]
    RoleBinding: _ClassVar[KubernetesObjectKind]
    Role: _ClassVar[KubernetesObjectKind]
    ReplicaSet: _ClassVar[KubernetesObjectKind]
    ServiceAccount: _ClassVar[KubernetesObjectKind]
    StorageClass: _ClassVar[KubernetesObjectKind]
    Secret: _ClassVar[KubernetesObjectKind]
    StatefulSet: _ClassVar[KubernetesObjectKind]
    User: _ClassVar[KubernetesObjectKind]
    Volume: _ClassVar[KubernetesObjectKind]
    HttpRoute: _ClassVar[KubernetesObjectKind]
kubernetes_object_kind_unspecified: KubernetesObjectKind
Deployment: KubernetesObjectKind
Pod: KubernetesObjectKind
Service: KubernetesObjectKind
ClusterRole: KubernetesObjectKind
ConfigMap: KubernetesObjectKind
ClusterRoleBinding: KubernetesObjectKind
CustomResourceDefinition: KubernetesObjectKind
CronJob: KubernetesObjectKind
DaemonSet: KubernetesObjectKind
Endpoints: KubernetesObjectKind
Group: KubernetesObjectKind
HorizontalPodAutoscaler: KubernetesObjectKind
Ingress: KubernetesObjectKind
Job: KubernetesObjectKind
LimitRange: KubernetesObjectKind
NetworkPolicy: KubernetesObjectKind
Namespace: KubernetesObjectKind
PodSecurityPolicy: KubernetesObjectKind
PersistentVolume: KubernetesObjectKind
PersistentVolumeClaim: KubernetesObjectKind
ResourceQuota: KubernetesObjectKind
RoleBinding: KubernetesObjectKind
Role: KubernetesObjectKind
ReplicaSet: KubernetesObjectKind
ServiceAccount: KubernetesObjectKind
StorageClass: KubernetesObjectKind
Secret: KubernetesObjectKind
StatefulSet: KubernetesObjectKind
User: KubernetesObjectKind
Volume: KubernetesObjectKind
HttpRoute: KubernetesObjectKind
