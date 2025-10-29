from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.infrahub.stackjob.v1 import api_pb2 as _api_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StackJobWorkflowInput(_message.Message):
    __slots__ = ("metadata", "stack_job", "workflow_config")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_CONFIG_FIELD_NUMBER: _ClassVar[int]
    metadata: _metadata_pb2.ApiResourceMetadata
    stack_job: _api_pb2.StackJob
    workflow_config: StackJobWorkflowConfig
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., stack_job: _Optional[_Union[_api_pb2.StackJob, _Mapping]] = ..., workflow_config: _Optional[_Union[StackJobWorkflowConfig, _Mapping]] = ...) -> None: ...

class StackJobWorkflowConfig(_message.Message):
    __slots__ = ("iac_operation_task_queue",)
    IAC_OPERATION_TASK_QUEUE_FIELD_NUMBER: _ClassVar[int]
    iac_operation_task_queue: str
    def __init__(self, iac_operation_task_queue: _Optional[str] = ...) -> None: ...
