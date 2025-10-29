from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from cloud.planton.apis.infrahub.infrapipeline.v1 import api_pb2 as _api_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InfraPipelineId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class ListInfraPipelinesByFiltersInput(_message.Message):
    __slots__ = ("page_info", "org", "infra_project_id")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    INFRA_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    org: str
    infra_project_id: str
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., org: _Optional[str] = ..., infra_project_id: _Optional[str] = ...) -> None: ...

class InfraPipelineList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.InfraPipeline]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_api_pb2.InfraPipeline, _Mapping]]] = ...) -> None: ...

class InfraPipelineDeploymentEnvironments(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.InfraPipelineDeploymentEnvironment]
    def __init__(self, entries: _Optional[_Iterable[_Union[_api_pb2.InfraPipelineDeploymentEnvironment, _Mapping]]] = ...) -> None: ...

class ResolveInfraPipelineManualGateRequest(_message.Message):
    __slots__ = ("infra_pipeline_id", "env", "manual_gate_decision")
    INFRA_PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    MANUAL_GATE_DECISION_FIELD_NUMBER: _ClassVar[int]
    infra_pipeline_id: str
    env: str
    manual_gate_decision: _workflow_pb2.WorkflowStepManualGateDecision
    def __init__(self, infra_pipeline_id: _Optional[str] = ..., env: _Optional[str] = ..., manual_gate_decision: _Optional[_Union[_workflow_pb2.WorkflowStepManualGateDecision, str]] = ...) -> None: ...

class RunGitCommitInfraPipelineRequest(_message.Message):
    __slots__ = ("infra_project_id", "commit_sha")
    INFRA_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    infra_project_id: str
    commit_sha: str
    def __init__(self, infra_project_id: _Optional[str] = ..., commit_sha: _Optional[str] = ...) -> None: ...
