from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SnowflakeDatabaseSpec(_message.Message):
    __slots__ = ("catalog", "comment", "data_retention_time_in_days", "default_ddl_collation", "drop_public_schema_on_creation", "enable_console_output", "external_volume", "is_transient", "log_level", "max_data_extension_time_in_days", "name", "quoted_identifiers_ignore_case", "replace_invalid_characters", "storage_serialization_policy", "suspend_task_after_num_failures", "task_auto_retry_attempts", "trace_level", "user_task")
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    DATA_RETENTION_TIME_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DDL_COLLATION_FIELD_NUMBER: _ClassVar[int]
    DROP_PUBLIC_SCHEMA_ON_CREATION_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CONSOLE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    IS_TRANSIENT_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    MAX_DATA_EXTENSION_TIME_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUOTED_IDENTIFIERS_IGNORE_CASE_FIELD_NUMBER: _ClassVar[int]
    REPLACE_INVALID_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_SERIALIZATION_POLICY_FIELD_NUMBER: _ClassVar[int]
    SUSPEND_TASK_AFTER_NUM_FAILURES_FIELD_NUMBER: _ClassVar[int]
    TASK_AUTO_RETRY_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    TRACE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    USER_TASK_FIELD_NUMBER: _ClassVar[int]
    catalog: str
    comment: str
    data_retention_time_in_days: int
    default_ddl_collation: str
    drop_public_schema_on_creation: bool
    enable_console_output: bool
    external_volume: str
    is_transient: bool
    log_level: str
    max_data_extension_time_in_days: int
    name: str
    quoted_identifiers_ignore_case: bool
    replace_invalid_characters: bool
    storage_serialization_policy: str
    suspend_task_after_num_failures: int
    task_auto_retry_attempts: int
    trace_level: str
    user_task: SnowflakeDatabaseUserTask
    def __init__(self, catalog: _Optional[str] = ..., comment: _Optional[str] = ..., data_retention_time_in_days: _Optional[int] = ..., default_ddl_collation: _Optional[str] = ..., drop_public_schema_on_creation: bool = ..., enable_console_output: bool = ..., external_volume: _Optional[str] = ..., is_transient: bool = ..., log_level: _Optional[str] = ..., max_data_extension_time_in_days: _Optional[int] = ..., name: _Optional[str] = ..., quoted_identifiers_ignore_case: bool = ..., replace_invalid_characters: bool = ..., storage_serialization_policy: _Optional[str] = ..., suspend_task_after_num_failures: _Optional[int] = ..., task_auto_retry_attempts: _Optional[int] = ..., trace_level: _Optional[str] = ..., user_task: _Optional[_Union[SnowflakeDatabaseUserTask, _Mapping]] = ...) -> None: ...

class SnowflakeDatabaseUserTask(_message.Message):
    __slots__ = ("managed_initial_warehouse_size", "minimum_trigger_interval_in_seconds", "timeout_ms")
    MANAGED_INITIAL_WAREHOUSE_SIZE_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_TRIGGER_INTERVAL_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    managed_initial_warehouse_size: str
    minimum_trigger_interval_in_seconds: int
    timeout_ms: int
    def __init__(self, managed_initial_warehouse_size: _Optional[str] = ..., minimum_trigger_interval_in_seconds: _Optional[int] = ..., timeout_ms: _Optional[int] = ...) -> None: ...
