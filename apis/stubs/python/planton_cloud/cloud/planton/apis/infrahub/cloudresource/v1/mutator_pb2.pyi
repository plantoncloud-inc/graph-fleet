from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceMutator(_message.Message):
    __slots__ = ("mutator_parent_kind", "mutator_parent_id", "mutator_kind", "mutator_id", "workflow_id", "author_id")
    MUTATOR_PARENT_KIND_FIELD_NUMBER: _ClassVar[int]
    MUTATOR_PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    MUTATOR_KIND_FIELD_NUMBER: _ClassVar[int]
    MUTATOR_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    mutator_parent_kind: _api_resource_kind_pb2.ApiResourceKind
    mutator_parent_id: str
    mutator_kind: _api_resource_kind_pb2.ApiResourceKind
    mutator_id: str
    workflow_id: str
    author_id: str
    def __init__(self, mutator_parent_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., mutator_parent_id: _Optional[str] = ..., mutator_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., mutator_id: _Optional[str] = ..., workflow_id: _Optional[str] = ..., author_id: _Optional[str] = ...) -> None: ...

class CloudResourceMutationResult(_message.Message):
    __slots__ = ("failed", "error_message", "cloud_resource_id", "version_id", "stack_job_id")
    FAILED_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    failed: bool
    error_message: str
    cloud_resource_id: str
    version_id: str
    stack_job_id: str
    def __init__(self, failed: bool = ..., error_message: _Optional[str] = ..., cloud_resource_id: _Optional[str] = ..., version_id: _Optional[str] = ..., stack_job_id: _Optional[str] = ...) -> None: ...
