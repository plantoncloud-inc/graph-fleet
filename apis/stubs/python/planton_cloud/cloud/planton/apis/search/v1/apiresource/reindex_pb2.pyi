from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchReindexRequest(_message.Message):
    __slots__ = ("org", "kinds")
    ORG_FIELD_NUMBER: _ClassVar[int]
    KINDS_FIELD_NUMBER: _ClassVar[int]
    org: str
    kinds: _containers.RepeatedScalarFieldContainer[_api_resource_kind_pb2.ApiResourceKind]
    def __init__(self, org: _Optional[str] = ..., kinds: _Optional[_Iterable[_Union[_api_resource_kind_pb2.ApiResourceKind, str]]] = ...) -> None: ...

class SearchReindexResponse(_message.Message):
    __slots__ = ("workflow_id", "org", "total_kinds", "kinds")
    WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    TOTAL_KINDS_FIELD_NUMBER: _ClassVar[int]
    KINDS_FIELD_NUMBER: _ClassVar[int]
    workflow_id: str
    org: str
    total_kinds: int
    kinds: _containers.RepeatedScalarFieldContainer[_api_resource_kind_pb2.ApiResourceKind]
    def __init__(self, workflow_id: _Optional[str] = ..., org: _Optional[str] = ..., total_kinds: _Optional[int] = ..., kinds: _Optional[_Iterable[_Union[_api_resource_kind_pb2.ApiResourceKind, str]]] = ...) -> None: ...
