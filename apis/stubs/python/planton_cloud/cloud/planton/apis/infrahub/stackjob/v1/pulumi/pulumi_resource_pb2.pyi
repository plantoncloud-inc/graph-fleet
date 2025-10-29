import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PulumiResource(_message.Message):
    __slots__ = ("stack_job_id", "ulid", "name", "urn", "custom", "delete", "type", "parent", "protect", "external", "init_errors", "provider", "pending_replacement", "retain_on_delete", "created", "modified", "source_position")
    STACK_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    ULID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URN_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PROTECT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    INIT_ERRORS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PENDING_REPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    RETAIN_ON_DELETE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    SOURCE_POSITION_FIELD_NUMBER: _ClassVar[int]
    stack_job_id: str
    ulid: str
    name: str
    urn: str
    custom: bool
    delete: bool
    type: str
    parent: str
    protect: bool
    external: bool
    init_errors: _containers.RepeatedScalarFieldContainer[str]
    provider: str
    pending_replacement: bool
    retain_on_delete: bool
    created: _timestamp_pb2.Timestamp
    modified: _timestamp_pb2.Timestamp
    source_position: str
    def __init__(self, stack_job_id: _Optional[str] = ..., ulid: _Optional[str] = ..., name: _Optional[str] = ..., urn: _Optional[str] = ..., custom: bool = ..., delete: bool = ..., type: _Optional[str] = ..., parent: _Optional[str] = ..., protect: bool = ..., external: bool = ..., init_errors: _Optional[_Iterable[str]] = ..., provider: _Optional[str] = ..., pending_replacement: bool = ..., retain_on_delete: bool = ..., created: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., modified: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., source_position: _Optional[str] = ...) -> None: ...
