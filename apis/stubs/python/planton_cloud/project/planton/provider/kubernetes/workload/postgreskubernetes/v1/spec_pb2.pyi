from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DEFAULT_CONTAINER_FIELD_NUMBER: _ClassVar[int]
default_container: _descriptor.FieldDescriptor

class PostgresKubernetesBackupConfig(_message.Message):
    __slots__ = ("s3_prefix", "backup_schedule", "enable_backup", "enable_restore", "enable_clone")
    S3_PREFIX_FIELD_NUMBER: _ClassVar[int]
    BACKUP_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_BACKUP_FIELD_NUMBER: _ClassVar[int]
    ENABLE_RESTORE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CLONE_FIELD_NUMBER: _ClassVar[int]
    s3_prefix: str
    backup_schedule: str
    enable_backup: bool
    enable_restore: bool
    enable_clone: bool
    def __init__(self, s3_prefix: _Optional[str] = ..., backup_schedule: _Optional[str] = ..., enable_backup: bool = ..., enable_restore: bool = ..., enable_clone: bool = ...) -> None: ...

class PostgresKubernetesSpec(_message.Message):
    __slots__ = ("container", "ingress", "backup_config")
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    BACKUP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    container: PostgresKubernetesContainer
    ingress: PostgresKubernetesIngress
    backup_config: PostgresKubernetesBackupConfig
    def __init__(self, container: _Optional[_Union[PostgresKubernetesContainer, _Mapping]] = ..., ingress: _Optional[_Union[PostgresKubernetesIngress, _Mapping]] = ..., backup_config: _Optional[_Union[PostgresKubernetesBackupConfig, _Mapping]] = ...) -> None: ...

class PostgresKubernetesContainer(_message.Message):
    __slots__ = ("replicas", "resources", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., disk_size: _Optional[str] = ...) -> None: ...

class PostgresKubernetesIngress(_message.Message):
    __slots__ = ("enabled", "hostname")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostname: str
    def __init__(self, enabled: bool = ..., hostname: _Optional[str] = ...) -> None: ...
