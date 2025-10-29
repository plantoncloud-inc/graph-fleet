from cloud.planton.apis.infrahub.stackjob.v1 import enum_pb2 as _enum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StackJobProgressIacOperationSnapshot(_message.Message):
    __slots__ = ("prelude_messages", "resource_row_map", "resource_diffs", "diagnostic_messages", "summary", "outputs")
    class ResourceRowMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: IacOperationResourceChangesSnapshotRow
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[IacOperationResourceChangesSnapshotRow, _Mapping]] = ...) -> None: ...
    class OutputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PRELUDE_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ROW_MAP_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_DIFFS_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTIC_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    prelude_messages: _containers.RepeatedScalarFieldContainer[str]
    resource_row_map: _containers.MessageMap[str, IacOperationResourceChangesSnapshotRow]
    resource_diffs: _containers.RepeatedScalarFieldContainer[str]
    diagnostic_messages: _containers.RepeatedCompositeFieldContainer[IacOperationDiagnosticMessage]
    summary: IacOperationSummarySnapshot
    outputs: _containers.ScalarMap[str, str]
    def __init__(self, prelude_messages: _Optional[_Iterable[str]] = ..., resource_row_map: _Optional[_Mapping[str, IacOperationResourceChangesSnapshotRow]] = ..., resource_diffs: _Optional[_Iterable[str]] = ..., diagnostic_messages: _Optional[_Iterable[_Union[IacOperationDiagnosticMessage, _Mapping]]] = ..., summary: _Optional[_Union[IacOperationSummarySnapshot, _Mapping]] = ..., outputs: _Optional[_Mapping[str, str]] = ...) -> None: ...

class IacOperationSummarySnapshot(_message.Message):
    __slots__ = ("duration_seconds", "unchanged_resource_count", "create_resource_count", "update_resource_count", "delete_resource_count", "replace_resource_count")
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    UNCHANGED_RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    CREATE_RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    DELETE_RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    REPLACE_RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    duration_seconds: int
    unchanged_resource_count: int
    create_resource_count: int
    update_resource_count: int
    delete_resource_count: int
    replace_resource_count: int
    def __init__(self, duration_seconds: _Optional[int] = ..., unchanged_resource_count: _Optional[int] = ..., create_resource_count: _Optional[int] = ..., update_resource_count: _Optional[int] = ..., delete_resource_count: _Optional[int] = ..., replace_resource_count: _Optional[int] = ...) -> None: ...

class IacOperationResourceChangesSnapshotRow(_message.Message):
    __slots__ = ("resource_kind", "resource_name", "status", "is_done", "is_failed", "elapsed_duration_seconds", "info")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_DONE_FIELD_NUMBER: _ClassVar[int]
    IS_FAILED_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    resource_kind: str
    resource_name: str
    status: str
    is_done: bool
    is_failed: bool
    elapsed_duration_seconds: int
    info: str
    def __init__(self, resource_kind: _Optional[str] = ..., resource_name: _Optional[str] = ..., status: _Optional[str] = ..., is_done: bool = ..., is_failed: bool = ..., elapsed_duration_seconds: _Optional[int] = ..., info: _Optional[str] = ...) -> None: ...

class IacOperationDiagnosticMessage(_message.Message):
    __slots__ = ("severity", "resource_urn", "message")
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_URN_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    severity: _enum_pb2.IacDiagnosticEventSeverityType
    resource_urn: str
    message: str
    def __init__(self, severity: _Optional[_Union[_enum_pb2.IacDiagnosticEventSeverityType, str]] = ..., resource_urn: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
