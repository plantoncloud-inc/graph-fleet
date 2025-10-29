import datetime

from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TektonPipelineDagEdgeReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    build_stage_edge_reason_unspecified: _ClassVar[TektonPipelineDagEdgeReason]
    run_after: _ClassVar[TektonPipelineDagEdgeReason]
    resource_from: _ClassVar[TektonPipelineDagEdgeReason]
    when_condition: _ClassVar[TektonPipelineDagEdgeReason]
build_stage_edge_reason_unspecified: TektonPipelineDagEdgeReason
run_after: TektonPipelineDagEdgeReason
resource_from: TektonPipelineDagEdgeReason
when_condition: TektonPipelineDagEdgeReason

class TektonPipelineDagTask(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TektonPipelineDagEdgeAttributes(_message.Message):
    __slots__ = ("reason", "resource_name", "index")
    REASON_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    reason: TektonPipelineDagEdgeReason
    resource_name: str
    index: _wrappers_pb2.Int32Value
    def __init__(self, reason: _Optional[_Union[TektonPipelineDagEdgeReason, str]] = ..., resource_name: _Optional[str] = ..., index: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ...) -> None: ...

class TektonPipelineDagDependencyEdge(_message.Message):
    __slots__ = ("source", "target", "attrs")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    ATTRS_FIELD_NUMBER: _ClassVar[int]
    source: TektonPipelineDagTask
    target: TektonPipelineDagTask
    attrs: TektonPipelineDagEdgeAttributes
    def __init__(self, source: _Optional[_Union[TektonPipelineDagTask, _Mapping]] = ..., target: _Optional[_Union[TektonPipelineDagTask, _Mapping]] = ..., attrs: _Optional[_Union[TektonPipelineDagEdgeAttributes, _Mapping]] = ...) -> None: ...

class TektonPipelineDagTaskExecution(_message.Message):
    __slots__ = ("task_uid", "start_time", "end_time", "status", "result", "error")
    TASK_UID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    task_uid: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    error: str
    def __init__(self, task_uid: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., error: _Optional[str] = ...) -> None: ...

class TektonPipelineDagTaskNode(_message.Message):
    __slots__ = ("id", "edges", "execution")
    ID_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_FIELD_NUMBER: _ClassVar[int]
    id: TektonPipelineDagTask
    edges: _containers.RepeatedCompositeFieldContainer[TektonPipelineDagDependencyEdge]
    execution: TektonPipelineDagTaskExecution
    def __init__(self, id: _Optional[_Union[TektonPipelineDagTask, _Mapping]] = ..., edges: _Optional[_Iterable[_Union[TektonPipelineDagDependencyEdge, _Mapping]]] = ..., execution: _Optional[_Union[TektonPipelineDagTaskExecution, _Mapping]] = ...) -> None: ...

class TektonPipelineDag(_message.Message):
    __slots__ = ("nodes", "topological_order")
    NODES_FIELD_NUMBER: _ClassVar[int]
    TOPOLOGICAL_ORDER_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[TektonPipelineDagTaskNode]
    topological_order: _containers.RepeatedCompositeFieldContainer[TektonPipelineDagTask]
    def __init__(self, nodes: _Optional[_Iterable[_Union[TektonPipelineDagTaskNode, _Mapping]]] = ..., topological_order: _Optional[_Iterable[_Union[TektonPipelineDagTask, _Mapping]]] = ...) -> None: ...
