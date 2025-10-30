from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MongodbAtlasSpec(_message.Message):
    __slots__ = ("cluster_config",)
    CLUSTER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    cluster_config: MongodbAtlasClusterConfig
    def __init__(self, cluster_config: _Optional[_Union[MongodbAtlasClusterConfig, _Mapping]] = ...) -> None: ...

class MongodbAtlasClusterConfig(_message.Message):
    __slots__ = ("project_id", "cluster_type", "electable_nodes", "priority", "read_only_nodes", "cloud_backup", "auto_scaling_disk_gb_enabled", "mongo_db_major_version", "provider_name", "provider_instance_size_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    ELECTABLE_NODES_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_NODES_FIELD_NUMBER: _ClassVar[int]
    CLOUD_BACKUP_FIELD_NUMBER: _ClassVar[int]
    AUTO_SCALING_DISK_GB_ENABLED_FIELD_NUMBER: _ClassVar[int]
    MONGO_DB_MAJOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_INSTANCE_SIZE_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    cluster_type: str
    electable_nodes: int
    priority: int
    read_only_nodes: int
    cloud_backup: bool
    auto_scaling_disk_gb_enabled: bool
    mongo_db_major_version: str
    provider_name: str
    provider_instance_size_name: str
    def __init__(self, project_id: _Optional[str] = ..., cluster_type: _Optional[str] = ..., electable_nodes: _Optional[int] = ..., priority: _Optional[int] = ..., read_only_nodes: _Optional[int] = ..., cloud_backup: bool = ..., auto_scaling_disk_gb_enabled: bool = ..., mongo_db_major_version: _Optional[str] = ..., provider_name: _Optional[str] = ..., provider_instance_size_name: _Optional[str] = ...) -> None: ...
