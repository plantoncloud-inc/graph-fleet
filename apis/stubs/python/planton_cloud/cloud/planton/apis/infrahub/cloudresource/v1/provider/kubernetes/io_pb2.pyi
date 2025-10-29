from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesClusterIdentifier(_message.Message):
    __slots__ = ("org", "env", "cluster_kind", "cluster_slug")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_KIND_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_SLUG_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    cluster_kind: _cloud_resource_kind_pb2.CloudResourceKind
    cluster_slug: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., cluster_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., cluster_slug: _Optional[str] = ...) -> None: ...
