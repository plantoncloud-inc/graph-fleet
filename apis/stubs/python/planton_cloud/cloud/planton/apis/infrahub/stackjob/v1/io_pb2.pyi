import datetime

from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from cloud.planton.apis.commons.workflow import workflow_pb2 as _workflow_pb2
from cloud.planton.apis.infrahub.stackjob.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.infrahub.stackjob.v1 import enum_pb2 as _enum_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StackJobId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class ListStackJobsByFiltersQueryInput(_message.Message):
    __slots__ = ("page_info", "org", "env", "cloud_resource_kind", "cloud_resource_id", "stack_job_operation", "status", "result")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_OPERATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    org: str
    env: str
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    cloud_resource_id: str
    stack_job_operation: _enum_pb2.StackJobOperationType
    status: _workflow_pb2.WorkflowExecutionStatus
    result: _workflow_pb2.WorkflowExecutionResult
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., org: _Optional[str] = ..., env: _Optional[str] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., cloud_resource_id: _Optional[str] = ..., stack_job_operation: _Optional[_Union[_enum_pb2.StackJobOperationType, str]] = ..., status: _Optional[_Union[_workflow_pb2.WorkflowExecutionStatus, str]] = ..., result: _Optional[_Union[_workflow_pb2.WorkflowExecutionResult, str]] = ...) -> None: ...

class StackJobList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.StackJob]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_api_pb2.StackJob, _Mapping]]] = ...) -> None: ...

class GetErrorResolutionRecommendationInput(_message.Message):
    __slots__ = ("stack_job_id", "error_message")
    STACK_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    stack_job_id: str
    error_message: str
    def __init__(self, stack_job_id: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class ServiceEnvStackJobs(_message.Message):
    __slots__ = ("entries",)
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _api_pb2.StackJob
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_api_pb2.StackJob, _Mapping]] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.MessageMap[str, _api_pb2.StackJob]
    def __init__(self, entries: _Optional[_Mapping[str, _api_pb2.StackJob]] = ...) -> None: ...

class IacResources(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.IacResource]
    def __init__(self, entries: _Optional[_Iterable[_Union[_api_pb2.IacResource, _Mapping]]] = ...) -> None: ...

class StreamStackJobsByOrgInput(_message.Message):
    __slots__ = ("org", "start_time", "end_time")
    ORG_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    org: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, org: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
