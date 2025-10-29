from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FgaTuple(_message.Message):
    __slots__ = ("audit", "id", "user_type", "user_id", "relation", "object_type", "object_id")
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    audit: _status_pb2.ApiResourceAuditInfo
    id: str
    user_type: str
    user_id: str
    relation: str
    object_type: str
    object_id: str
    def __init__(self, audit: _Optional[_Union[_status_pb2.ApiResourceAuditInfo, _Mapping]] = ..., id: _Optional[str] = ..., user_type: _Optional[str] = ..., user_id: _Optional[str] = ..., relation: _Optional[str] = ..., object_type: _Optional[str] = ..., object_id: _Optional[str] = ...) -> None: ...
