from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from project.planton.shared.kubernetes import target_cluster_pb2 as _target_cluster_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostgresOperatorKubernetesBackupR2Config(_message.Message):
    __slots__ = ("cloudflare_account_id", "bucket_name", "access_key_id", "secret_access_key")
    CLOUDFLARE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    cloudflare_account_id: str
    bucket_name: str
    access_key_id: str
    secret_access_key: str
    def __init__(self, cloudflare_account_id: _Optional[str] = ..., bucket_name: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ...) -> None: ...

class PostgresOperatorKubernetesBackupConfig(_message.Message):
    __slots__ = ("r2_config", "s3_prefix_template", "backup_schedule", "enable_wal_g_backup", "enable_wal_g_restore", "enable_clone_wal_g_restore")
    R2_CONFIG_FIELD_NUMBER: _ClassVar[int]
    S3_PREFIX_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    BACKUP_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_WAL_G_BACKUP_FIELD_NUMBER: _ClassVar[int]
    ENABLE_WAL_G_RESTORE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CLONE_WAL_G_RESTORE_FIELD_NUMBER: _ClassVar[int]
    r2_config: PostgresOperatorKubernetesBackupR2Config
    s3_prefix_template: str
    backup_schedule: str
    enable_wal_g_backup: bool
    enable_wal_g_restore: bool
    enable_clone_wal_g_restore: bool
    def __init__(self, r2_config: _Optional[_Union[PostgresOperatorKubernetesBackupR2Config, _Mapping]] = ..., s3_prefix_template: _Optional[str] = ..., backup_schedule: _Optional[str] = ..., enable_wal_g_backup: bool = ..., enable_wal_g_restore: bool = ..., enable_clone_wal_g_restore: bool = ...) -> None: ...

class PostgresOperatorKubernetesSpec(_message.Message):
    __slots__ = ("target_cluster", "container", "backup_config")
    TARGET_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    BACKUP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    target_cluster: _target_cluster_pb2.KubernetesAddonTargetCluster
    container: PostgresOperatorKubernetesSpecContainer
    backup_config: PostgresOperatorKubernetesBackupConfig
    def __init__(self, target_cluster: _Optional[_Union[_target_cluster_pb2.KubernetesAddonTargetCluster, _Mapping]] = ..., container: _Optional[_Union[PostgresOperatorKubernetesSpecContainer, _Mapping]] = ..., backup_config: _Optional[_Union[PostgresOperatorKubernetesBackupConfig, _Mapping]] = ...) -> None: ...

class PostgresOperatorKubernetesSpecContainer(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _kubernetes_pb2.ContainerResources
    def __init__(self, resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ...) -> None: ...
