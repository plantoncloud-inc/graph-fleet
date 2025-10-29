import datetime

from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from cloud.planton.apis.infrahub.stackjob.v1 import snapshot_pb2 as _snapshot_pb2
from cloud.planton.apis.infrahub.stackjob.v1 import spec_pb2 as _spec_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StackJob(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.ApiResourceMetadata
    spec: _spec_pb2.StackJobSpec
    status: StackJobStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[_spec_pb2.StackJobSpec, _Mapping]] = ..., status: _Optional[_Union[StackJobStatus, _Mapping]] = ...) -> None: ...

class StackJobStatus(_message.Message):
    __slots__ = ("audit", "progress", "iac_operations", "iac_resources")
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    IAC_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    IAC_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    audit: _status_pb2.ApiResourceAudit
    progress: StackJobProgressStatus
    iac_operations: StackJobStatusIacOperationsState
    iac_resources: _containers.RepeatedCompositeFieldContainer[IacResource]
    def __init__(self, audit: _Optional[_Union[_status_pb2.ApiResourceAudit, _Mapping]] = ..., progress: _Optional[_Union[StackJobProgressStatus, _Mapping]] = ..., iac_operations: _Optional[_Union[StackJobStatusIacOperationsState, _Mapping]] = ..., iac_resources: _Optional[_Iterable[_Union[IacResource, _Mapping]]] = ...) -> None: ...

class StackJobProgressStatus(_message.Message):
    __slots__ = ("start_time", "end_time", "status", "result", "errors")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., errors: _Optional[_Iterable[str]] = ...) -> None: ...

class StackJobProgressIacOperationState(_message.Message):
    __slots__ = ("id", "is_required", "is_approved", "status", "result", "start_time", "end_time", "errors", "snapshot")
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    IS_APPROVED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    id: str
    is_required: bool
    is_approved: bool
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    errors: _containers.RepeatedScalarFieldContainer[str]
    snapshot: _snapshot_pb2.StackJobProgressIacOperationSnapshot
    def __init__(self, id: _Optional[str] = ..., is_required: bool = ..., is_approved: bool = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., errors: _Optional[_Iterable[str]] = ..., snapshot: _Optional[_Union[_snapshot_pb2.StackJobProgressIacOperationSnapshot, _Mapping]] = ...) -> None: ...

class StackJobStatusIacOperationsState(_message.Message):
    __slots__ = ("init", "refresh", "update_preview", "destroy_preview", "update", "destroy")
    INIT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_FIELD_NUMBER: _ClassVar[int]
    UPDATE_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    DESTROY_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    DESTROY_FIELD_NUMBER: _ClassVar[int]
    init: StackJobProgressIacOperationState
    refresh: StackJobProgressIacOperationState
    update_preview: StackJobProgressIacOperationState
    destroy_preview: StackJobProgressIacOperationState
    update: StackJobProgressIacOperationState
    destroy: StackJobProgressIacOperationState
    def __init__(self, init: _Optional[_Union[StackJobProgressIacOperationState, _Mapping]] = ..., refresh: _Optional[_Union[StackJobProgressIacOperationState, _Mapping]] = ..., update_preview: _Optional[_Union[StackJobProgressIacOperationState, _Mapping]] = ..., destroy_preview: _Optional[_Union[StackJobProgressIacOperationState, _Mapping]] = ..., update: _Optional[_Union[StackJobProgressIacOperationState, _Mapping]] = ..., destroy: _Optional[_Union[StackJobProgressIacOperationState, _Mapping]] = ...) -> None: ...

class IacResource(_message.Message):
    __slots__ = ("address", "resource_type", "provider", "logical_name", "resource_external_id")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    resource_type: str
    provider: str
    logical_name: str
    resource_external_id: str
    def __init__(self, address: _Optional[str] = ..., resource_type: _Optional[str] = ..., provider: _Optional[str] = ..., logical_name: _Optional[str] = ..., resource_external_id: _Optional[str] = ...) -> None: ...
