from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceVersionSpec(_message.Message):
    __slots__ = ("resource_kind", "resource_id", "original_state_yaml", "new_state_yaml", "diff_unified_format", "api_resource_event_type", "stack_job_id", "previous_version_id")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_STATE_YAML_FIELD_NUMBER: _ClassVar[int]
    NEW_STATE_YAML_FIELD_NUMBER: _ClassVar[int]
    DIFF_UNIFIED_FORMAT_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    resource_kind: _api_resource_kind_pb2.ApiResourceKind
    resource_id: str
    original_state_yaml: str
    new_state_yaml: str
    diff_unified_format: str
    api_resource_event_type: str
    stack_job_id: str
    previous_version_id: str
    def __init__(self, resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., resource_id: _Optional[str] = ..., original_state_yaml: _Optional[str] = ..., new_state_yaml: _Optional[str] = ..., diff_unified_format: _Optional[str] = ..., api_resource_event_type: _Optional[str] = ..., stack_job_id: _Optional[str] = ..., previous_version_id: _Optional[str] = ...) -> None: ...
