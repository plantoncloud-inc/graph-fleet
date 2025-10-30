from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesCloudResourceCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    kubernetes_cloud_resource_category_unspecified: _ClassVar[KubernetesCloudResourceCategory]
    addon: _ClassVar[KubernetesCloudResourceCategory]
    workload: _ClassVar[KubernetesCloudResourceCategory]
kubernetes_cloud_resource_category_unspecified: KubernetesCloudResourceCategory
addon: KubernetesCloudResourceCategory
workload: KubernetesCloudResourceCategory
