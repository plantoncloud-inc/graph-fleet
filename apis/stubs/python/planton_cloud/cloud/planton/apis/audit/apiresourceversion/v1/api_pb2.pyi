from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.audit.apiresourceversion.v1 import spec_pb2 as _spec_pb2
from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceVersion(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.ApiResourceMetadata
    spec: _spec_pb2.ApiResourceVersionSpec
    status: ApiResourceVersionStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[_spec_pb2.ApiResourceVersionSpec, _Mapping]] = ..., status: _Optional[_Union[ApiResourceVersionStatus, _Mapping]] = ...) -> None: ...

class ApiResourceVersionStatus(_message.Message):
    __slots__ = ("audit", "stack_job_progress_status", "stack_job_progress_result")
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_PROGRESS_STATUS_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_PROGRESS_RESULT_FIELD_NUMBER: _ClassVar[int]
    audit: _status_pb2.ApiResourceAudit
    stack_job_progress_status: _workflow_pb2.WorkflowExecutionStatus
    stack_job_progress_result: _workflow_pb2.WorkflowExecutionResult
    def __init__(self, audit: _Optional[_Union[_status_pb2.ApiResourceAudit, _Mapping]] = ..., stack_job_progress_status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., stack_job_progress_result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ...) -> None: ...
