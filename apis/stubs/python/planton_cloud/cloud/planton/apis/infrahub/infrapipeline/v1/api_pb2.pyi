import datetime

from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from cloud.planton.apis.infrahub.cloudresource.v1 import dag_pb2 as _dag_pb2
from cloud.planton.apis.infrahub.infrapipeline.v1 import spec_pb2 as _spec_pb2
from cloud.planton.apis.integration.tekton import tekton_pipeline_dag_pb2 as _tekton_pipeline_dag_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InfraPipeline(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.ApiResourceMetadata
    spec: _spec_pb2.InfraPipelineSpec
    status: InfraPipelineStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[_spec_pb2.InfraPipelineSpec, _Mapping]] = ..., status: _Optional[_Union[InfraPipelineStatus, _Mapping]] = ...) -> None: ...

class InfraPipelineStatus(_message.Message):
    __slots__ = ("audit", "start_time", "end_time", "progress_status", "progress_result", "status_reason", "build_stage", "deployment_stage")
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_RESULT_FIELD_NUMBER: _ClassVar[int]
    STATUS_REASON_FIELD_NUMBER: _ClassVar[int]
    BUILD_STAGE_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_STAGE_FIELD_NUMBER: _ClassVar[int]
    audit: _status_pb2.ApiResourceAudit
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    progress_status: _workflow_pb2.WorkflowExecutionStatus
    progress_result: _workflow_pb2.WorkflowExecutionResult
    status_reason: str
    build_stage: InfraPipelineBuildStage
    deployment_stage: InfraPipelineDeploymentStage
    def __init__(self, audit: _Optional[_Union[_status_pb2.ApiResourceAudit, _Mapping]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., progress_status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., progress_result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., status_reason: _Optional[str] = ..., build_stage: _Optional[_Union[InfraPipelineBuildStage, _Mapping]] = ..., deployment_stage: _Optional[_Union[InfraPipelineDeploymentStage, _Mapping]] = ...) -> None: ...

class InfraPipelineBuildStage(_message.Message):
    __slots__ = ("start_time", "end_time", "status", "result", "status_reason", "github_check_run_id", "dag", "tasks")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STATUS_REASON_FIELD_NUMBER: _ClassVar[int]
    GITHUB_CHECK_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    DAG_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    status_reason: str
    github_check_run_id: int
    dag: _tekton_pipeline_dag_pb2.TektonPipelineDag
    tasks: _containers.RepeatedCompositeFieldContainer[InfraPipelineBuildTask]
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., status_reason: _Optional[str] = ..., github_check_run_id: _Optional[int] = ..., dag: _Optional[_Union[_tekton_pipeline_dag_pb2.TektonPipelineDag, _Mapping]] = ..., tasks: _Optional[_Iterable[_Union[InfraPipelineBuildTask, _Mapping]]] = ...) -> None: ...

class InfraPipelineDeploymentStage(_message.Message):
    __slots__ = ("start_time", "end_time", "status", "result", "status_reason", "environments")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STATUS_REASON_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    status_reason: str
    environments: _containers.RepeatedCompositeFieldContainer[InfraPipelineDeploymentEnvironment]
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., status_reason: _Optional[str] = ..., environments: _Optional[_Iterable[_Union[InfraPipelineDeploymentEnvironment, _Mapping]]] = ...) -> None: ...

class InfraPipelineDeploymentEnvironment(_message.Message):
    __slots__ = ("name", "position", "start_time", "end_time", "status", "result", "error", "diagnostic_message", "env", "yaml_manifest", "cloud_resource_dag", "requires_manual_gate", "manual_gate_decision")
    NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTIC_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    YAML_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_DAG_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_MANUAL_GATE_FIELD_NUMBER: _ClassVar[int]
    MANUAL_GATE_DECISION_FIELD_NUMBER: _ClassVar[int]
    name: str
    position: int
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    error: str
    diagnostic_message: str
    env: str
    yaml_manifest: str
    cloud_resource_dag: _dag_pb2.CloudResourceDag
    requires_manual_gate: bool
    manual_gate_decision: _workflow_pb2.WorkflowStepManualGateDecision
    def __init__(self, name: _Optional[str] = ..., position: _Optional[int] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., error: _Optional[str] = ..., diagnostic_message: _Optional[str] = ..., env: _Optional[str] = ..., yaml_manifest: _Optional[str] = ..., cloud_resource_dag: _Optional[_Union[_dag_pb2.CloudResourceDag, _Mapping]] = ..., requires_manual_gate: bool = ..., manual_gate_decision: _Optional[_Union[_workflow_pb2.WorkflowStepManualGateDecision, str]] = ...) -> None: ...

class InfraPipelineBuildTask(_message.Message):
    __slots__ = ("name", "depends_on", "start_time", "end_time", "status", "result", "error", "diagnostic_message", "pod_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEPENDS_ON_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTIC_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    POD_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    depends_on: _containers.RepeatedScalarFieldContainer[str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    error: str
    diagnostic_message: str
    pod_id: str
    def __init__(self, name: _Optional[str] = ..., depends_on: _Optional[_Iterable[str]] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., error: _Optional[str] = ..., diagnostic_message: _Optional[str] = ..., pod_id: _Optional[str] = ...) -> None: ...
