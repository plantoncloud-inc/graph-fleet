import datetime

from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from cloud.planton.apis.infrahub.stackjob.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.infrahub.stackjob.v1 import enum_pb2 as _enum_pb2
from cloud.planton.apis.infrahub.stackjob.v1.pulumi import payload_pb2 as _payload_pb2
from cloud.planton.apis.infrahub.stackjob.v1.terraform import payload_pb2 as _payload_pb2_1
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StackJobProgressEvent(_message.Message):
    __slots__ = ("timestamp", "stack_job_operation", "event_type", "job_status_changed_event_payload", "iac_module_repo_setup_log_lines", "iac_operation_status_payload", "iac_stack_resources_payload", "iac_stack_outputs_payload", "terraform_engine_event_payload", "pulumi_engine_event_payload")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_OPERATION_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    JOB_STATUS_CHANGED_EVENT_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    IAC_MODULE_REPO_SETUP_LOG_LINES_FIELD_NUMBER: _ClassVar[int]
    IAC_OPERATION_STATUS_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    IAC_STACK_RESOURCES_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    IAC_STACK_OUTPUTS_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TERRAFORM_ENGINE_EVENT_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    PULUMI_ENGINE_EVENT_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    stack_job_operation: _enum_pb2.StackJobOperationType
    event_type: _enum_pb2.StackJobProgressEventType
    job_status_changed_event_payload: StackJobProgressJobStatusChangedPayload
    iac_module_repo_setup_log_lines: _containers.RepeatedScalarFieldContainer[str]
    iac_operation_status_payload: StackJobProgressIacOperationStatusPayload
    iac_stack_resources_payload: IacStackResourcesPayload
    iac_stack_outputs_payload: IacStackOutputsPayload
    terraform_engine_event_payload: _payload_pb2_1.TerraformEngineEventPayload
    pulumi_engine_event_payload: _payload_pb2.PulumiEngineEventPayload
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., stack_job_operation: _Optional[_Union[_enum_pb2.StackJobOperationType, str]] = ..., event_type: _Optional[_Union[_enum_pb2.StackJobProgressEventType, str]] = ..., job_status_changed_event_payload: _Optional[_Union[StackJobProgressJobStatusChangedPayload, _Mapping]] = ..., iac_module_repo_setup_log_lines: _Optional[_Iterable[str]] = ..., iac_operation_status_payload: _Optional[_Union[StackJobProgressIacOperationStatusPayload, _Mapping]] = ..., iac_stack_resources_payload: _Optional[_Union[IacStackResourcesPayload, _Mapping]] = ..., iac_stack_outputs_payload: _Optional[_Union[IacStackOutputsPayload, _Mapping]] = ..., terraform_engine_event_payload: _Optional[_Union[_payload_pb2_1.TerraformEngineEventPayload, _Mapping]] = ..., pulumi_engine_event_payload: _Optional[_Union[_payload_pb2.PulumiEngineEventPayload, _Mapping]] = ...) -> None: ...

class StackJobProgressIacOperationStatusPayload(_message.Message):
    __slots__ = ("status", "result", "errors")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., errors: _Optional[_Iterable[str]] = ...) -> None: ...

class StackJobProgressJobStatusChangedPayload(_message.Message):
    __slots__ = ("status", "result", "failed_reason")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    FAILED_REASON_FIELD_NUMBER: _ClassVar[int]
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    failed_reason: str
    def __init__(self, status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., failed_reason: _Optional[str] = ...) -> None: ...

class IacStackOutputsPayload(_message.Message):
    __slots__ = ("outputs",)
    class OutputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.ScalarMap[str, str]
    def __init__(self, outputs: _Optional[_Mapping[str, str]] = ...) -> None: ...

class IacStackResourcesPayload(_message.Message):
    __slots__ = ("iac_resources",)
    IAC_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    iac_resources: _containers.RepeatedCompositeFieldContainer[_api_pb2.IacResource]
    def __init__(self, iac_resources: _Optional[_Iterable[_Union[_api_pb2.IacResource, _Mapping]]] = ...) -> None: ...
