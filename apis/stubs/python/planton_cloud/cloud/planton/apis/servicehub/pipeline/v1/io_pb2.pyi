import datetime

from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from cloud.planton.apis.servicehub.pipeline.v1 import api_pb2 as _api_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class ListPipelinesByFiltersInput(_message.Message):
    __slots__ = ("page_info", "org", "service_id")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    org: str
    service_id: str
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., org: _Optional[str] = ..., service_id: _Optional[str] = ...) -> None: ...

class PipelineList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.Pipeline]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_api_pb2.Pipeline, _Mapping]]] = ...) -> None: ...

class PipelineDeploymentTasks(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.PipelineDeploymentTask]
    def __init__(self, entries: _Optional[_Iterable[_Union[_api_pb2.PipelineDeploymentTask, _Mapping]]] = ...) -> None: ...

class ResolvePipelineManualGateRequest(_message.Message):
    __slots__ = ("pipeline_id", "deployment_task_name", "manual_gate_decision")
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_TASK_NAME_FIELD_NUMBER: _ClassVar[int]
    MANUAL_GATE_DECISION_FIELD_NUMBER: _ClassVar[int]
    pipeline_id: str
    deployment_task_name: str
    manual_gate_decision: _workflow_pb2.WorkflowStepManualGateDecision
    def __init__(self, pipeline_id: _Optional[str] = ..., deployment_task_name: _Optional[str] = ..., manual_gate_decision: _Optional[_Union[_workflow_pb2.WorkflowStepManualGateDecision, str]] = ...) -> None: ...

class RunGitCommitPipelineRequest(_message.Message):
    __slots__ = ("service_id", "commit_sha")
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    service_id: str
    commit_sha: str
    def __init__(self, service_id: _Optional[str] = ..., commit_sha: _Optional[str] = ...) -> None: ...

class StreamPipelinesByOrgInput(_message.Message):
    __slots__ = ("org", "start_time", "end_time")
    ORG_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    org: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, org: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListServiceRepoPipelineFilesInput(_message.Message):
    __slots__ = ("service_id", "branch")
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    service_id: str
    branch: str
    def __init__(self, service_id: _Optional[str] = ..., branch: _Optional[str] = ...) -> None: ...

class ServiceRepoPipelineFile(_message.Message):
    __slots__ = ("path", "sha", "content", "encoding", "display_name")
    PATH_FIELD_NUMBER: _ClassVar[int]
    SHA_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    path: str
    sha: str
    content: bytes
    encoding: str
    display_name: str
    def __init__(self, path: _Optional[str] = ..., sha: _Optional[str] = ..., content: _Optional[bytes] = ..., encoding: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...

class ServiceRepoPipelineFileList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[ServiceRepoPipelineFile]
    def __init__(self, entries: _Optional[_Iterable[_Union[ServiceRepoPipelineFile, _Mapping]]] = ...) -> None: ...

class UpdateServiceRepoPipelineFileInput(_message.Message):
    __slots__ = ("service_id", "path", "content", "expected_base_sha", "commit_message", "branch")
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_BASE_SHA_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    service_id: str
    path: str
    content: bytes
    expected_base_sha: str
    commit_message: str
    branch: str
    def __init__(self, service_id: _Optional[str] = ..., path: _Optional[str] = ..., content: _Optional[bytes] = ..., expected_base_sha: _Optional[str] = ..., commit_message: _Optional[str] = ..., branch: _Optional[str] = ...) -> None: ...

class UpdateServiceRepoPipelineFileResponse(_message.Message):
    __slots__ = ("new_sha", "commit_sha", "branch")
    NEW_SHA_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    new_sha: str
    commit_sha: str
    branch: str
    def __init__(self, new_sha: _Optional[str] = ..., commit_sha: _Optional[str] = ..., branch: _Optional[str] = ...) -> None: ...
