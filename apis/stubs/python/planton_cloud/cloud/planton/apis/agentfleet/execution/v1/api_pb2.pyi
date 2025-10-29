from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.agentfleet.execution.v1 import enum_pb2 as _enum_pb2
from cloud.planton.apis.agentfleet.execution.v1 import spec_pb2 as _spec_pb2
from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Execution(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.ApiResourceMetadata
    spec: _spec_pb2.ExecutionSpec
    status: ExecutionStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[_spec_pb2.ExecutionSpec, _Mapping]] = ..., status: _Optional[_Union[ExecutionStatus, _Mapping]] = ...) -> None: ...

class ExecutionStatus(_message.Message):
    __slots__ = ("audit", "messages", "todos", "files")
    class TodosEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TodoItem
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[TodoItem, _Mapping]] = ...) -> None: ...
    class FilesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FileData
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FileData, _Mapping]] = ...) -> None: ...
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TODOS_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    audit: _status_pb2.ApiResourceAudit
    messages: _containers.RepeatedCompositeFieldContainer[_spec_pb2.AgentMessage]
    todos: _containers.MessageMap[str, TodoItem]
    files: _containers.MessageMap[str, FileData]
    def __init__(self, audit: _Optional[_Union[_status_pb2.ApiResourceAudit, _Mapping]] = ..., messages: _Optional[_Iterable[_Union[_spec_pb2.AgentMessage, _Mapping]]] = ..., todos: _Optional[_Mapping[str, TodoItem]] = ..., files: _Optional[_Mapping[str, FileData]] = ...) -> None: ...

class TodoItem(_message.Message):
    __slots__ = ("id", "content", "status", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    content: str
    status: _enum_pb2.TodoStatus
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., content: _Optional[str] = ..., status: _Optional[_Union[_enum_pb2.TodoStatus, str]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class FileData(_message.Message):
    __slots__ = ("content", "created_at", "modified_at", "mime_type")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    content: _containers.RepeatedScalarFieldContainer[str]
    created_at: str
    modified_at: str
    mime_type: str
    def __init__(self, content: _Optional[_Iterable[str]] = ..., created_at: _Optional[str] = ..., modified_at: _Optional[str] = ..., mime_type: _Optional[str] = ...) -> None: ...
