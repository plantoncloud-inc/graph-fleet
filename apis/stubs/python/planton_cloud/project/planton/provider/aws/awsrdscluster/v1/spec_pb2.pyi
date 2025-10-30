from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsRdsClusterSpec(_message.Message):
    __slots__ = ("subnet_ids", "db_subnet_group_name", "security_group_ids", "allowed_cidr_blocks", "associate_security_group_ids", "database_name", "manage_master_user_password", "master_user_secret_kms_key_id", "username", "password", "port", "engine", "engine_version", "storage_encrypted", "kms_key_id", "enabled_cloudwatch_logs_exports", "deletion_protection", "preferred_maintenance_window", "backup_retention_period", "preferred_backup_window", "copy_tags_to_snapshot", "skip_final_snapshot", "final_snapshot_identifier", "iam_database_authentication_enabled", "enable_http_endpoint", "serverless_v2_scaling", "snapshot_identifier", "replication_source_identifier", "db_cluster_parameter_group_name", "parameters", "vpc_id", "engine_mode", "storage_type")
    SUBNET_IDS_FIELD_NUMBER: _ClassVar[int]
    DB_SUBNET_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_CIDR_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    ASSOCIATE_SECURITY_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    MANAGE_MASTER_USER_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    MASTER_USER_SECRET_KMS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    KMS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_CLOUDWATCH_LOGS_EXPORTS_FIELD_NUMBER: _ClassVar[int]
    DELETION_PROTECTION_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    BACKUP_RETENTION_PERIOD_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_BACKUP_WINDOW_FIELD_NUMBER: _ClassVar[int]
    COPY_TAGS_TO_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    SKIP_FINAL_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    FINAL_SNAPSHOT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    IAM_DATABASE_AUTHENTICATION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ENABLE_HTTP_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    SERVERLESS_V2_SCALING_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    REPLICATION_SOURCE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DB_CLUSTER_PARAMETER_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VPC_ID_FIELD_NUMBER: _ClassVar[int]
    ENGINE_MODE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    subnet_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    db_subnet_group_name: _foreign_key_pb2.StringValueOrRef
    security_group_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    allowed_cidr_blocks: _containers.RepeatedScalarFieldContainer[str]
    associate_security_group_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    database_name: str
    manage_master_user_password: bool
    master_user_secret_kms_key_id: _foreign_key_pb2.StringValueOrRef
    username: str
    password: str
    port: int
    engine: str
    engine_version: str
    storage_encrypted: bool
    kms_key_id: _foreign_key_pb2.StringValueOrRef
    enabled_cloudwatch_logs_exports: _containers.RepeatedScalarFieldContainer[str]
    deletion_protection: bool
    preferred_maintenance_window: str
    backup_retention_period: int
    preferred_backup_window: str
    copy_tags_to_snapshot: bool
    skip_final_snapshot: bool
    final_snapshot_identifier: str
    iam_database_authentication_enabled: bool
    enable_http_endpoint: bool
    serverless_v2_scaling: AwsRdsClusterServerlessV2ScalingConfiguration
    snapshot_identifier: str
    replication_source_identifier: str
    db_cluster_parameter_group_name: str
    parameters: _containers.RepeatedCompositeFieldContainer[AwsRdsClusterParameter]
    vpc_id: _foreign_key_pb2.StringValueOrRef
    engine_mode: str
    storage_type: str
    def __init__(self, subnet_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., db_subnet_group_name: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., security_group_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., allowed_cidr_blocks: _Optional[_Iterable[str]] = ..., associate_security_group_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., database_name: _Optional[str] = ..., manage_master_user_password: bool = ..., master_user_secret_kms_key_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., port: _Optional[int] = ..., engine: _Optional[str] = ..., engine_version: _Optional[str] = ..., storage_encrypted: bool = ..., kms_key_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., enabled_cloudwatch_logs_exports: _Optional[_Iterable[str]] = ..., deletion_protection: bool = ..., preferred_maintenance_window: _Optional[str] = ..., backup_retention_period: _Optional[int] = ..., preferred_backup_window: _Optional[str] = ..., copy_tags_to_snapshot: bool = ..., skip_final_snapshot: bool = ..., final_snapshot_identifier: _Optional[str] = ..., iam_database_authentication_enabled: bool = ..., enable_http_endpoint: bool = ..., serverless_v2_scaling: _Optional[_Union[AwsRdsClusterServerlessV2ScalingConfiguration, _Mapping]] = ..., snapshot_identifier: _Optional[str] = ..., replication_source_identifier: _Optional[str] = ..., db_cluster_parameter_group_name: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[AwsRdsClusterParameter, _Mapping]]] = ..., vpc_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., engine_mode: _Optional[str] = ..., storage_type: _Optional[str] = ...) -> None: ...

class AwsRdsClusterParameter(_message.Message):
    __slots__ = ("apply_method", "name", "value")
    APPLY_METHOD_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    apply_method: str
    name: str
    value: str
    def __init__(self, apply_method: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class AwsRdsClusterServerlessV2ScalingConfiguration(_message.Message):
    __slots__ = ("min_capacity", "max_capacity")
    MIN_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    MAX_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    min_capacity: float
    max_capacity: float
    def __init__(self, min_capacity: _Optional[float] = ..., max_capacity: _Optional[float] = ...) -> None: ...
