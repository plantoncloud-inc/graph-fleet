import datetime

from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceDagNodeRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    cloud_resource_dag_node_role_unspecified: _ClassVar[CloudResourceDagNodeRole]
    resource: _ClassVar[CloudResourceDagNodeRole]
    group: _ClassVar[CloudResourceDagNodeRole]
cloud_resource_dag_node_role_unspecified: CloudResourceDagNodeRole
resource: CloudResourceDagNodeRole
group: CloudResourceDagNodeRole

class CloudResourceDagResource(_message.Message):
    __slots__ = ("kind", "env", "slug")
    KIND_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    kind: _cloud_resource_kind_pb2.CloudResourceKind
    env: str
    slug: str
    def __init__(self, kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., env: _Optional[str] = ..., slug: _Optional[str] = ...) -> None: ...

class CloudResourceDagEdgeAttributes(_message.Message):
    __slots__ = ("ref_field_path", "source_field_path", "selector", "index")
    REF_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ref_field_path: str
    source_field_path: str
    selector: str
    index: _wrappers_pb2.Int32Value
    def __init__(self, ref_field_path: _Optional[str] = ..., source_field_path: _Optional[str] = ..., selector: _Optional[str] = ..., index: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ...) -> None: ...

class CloudResourceDagDependencyEdge(_message.Message):
    __slots__ = ("target", "attrs")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    ATTRS_FIELD_NUMBER: _ClassVar[int]
    target: CloudResourceDagResource
    attrs: CloudResourceDagEdgeAttributes
    def __init__(self, target: _Optional[_Union[CloudResourceDagResource, _Mapping]] = ..., attrs: _Optional[_Union[CloudResourceDagEdgeAttributes, _Mapping]] = ...) -> None: ...

class CloudResourceDagNode(_message.Message):
    __slots__ = ("id", "edges", "execution", "role", "group_label", "parent_group_path", "resource_group")
    ID_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    GROUP_LABEL_FIELD_NUMBER: _ClassVar[int]
    PARENT_GROUP_PATH_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    id: CloudResourceDagResource
    edges: _containers.RepeatedCompositeFieldContainer[CloudResourceDagDependencyEdge]
    execution: CloudResourceDagNodeExecution
    role: CloudResourceDagNodeRole
    group_label: str
    parent_group_path: str
    resource_group: str
    def __init__(self, id: _Optional[_Union[CloudResourceDagResource, _Mapping]] = ..., edges: _Optional[_Iterable[_Union[CloudResourceDagDependencyEdge, _Mapping]]] = ..., execution: _Optional[_Union[CloudResourceDagNodeExecution, _Mapping]] = ..., role: _Optional[_Union[CloudResourceDagNodeRole, str]] = ..., group_label: _Optional[str] = ..., parent_group_path: _Optional[str] = ..., resource_group: _Optional[str] = ...) -> None: ...

class CloudResourceDag(_message.Message):
    __slots__ = ("nodes", "topological_order")
    NODES_FIELD_NUMBER: _ClassVar[int]
    TOPOLOGICAL_ORDER_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[CloudResourceDagNode]
    topological_order: _containers.RepeatedCompositeFieldContainer[CloudResourceDagResource]
    def __init__(self, nodes: _Optional[_Iterable[_Union[CloudResourceDagNode, _Mapping]]] = ..., topological_order: _Optional[_Iterable[_Union[CloudResourceDagResource, _Mapping]]] = ...) -> None: ...

class CloudResourceDagNodeExecution(_message.Message):
    __slots__ = ("start_time", "end_time", "status", "result", "cloud_resource_kind", "cloud_resource_id", "stack_job_id")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    cloud_resource_id: str
    stack_job_id: str
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., cloud_resource_id: _Optional[str] = ..., stack_job_id: _Optional[str] = ...) -> None: ...
