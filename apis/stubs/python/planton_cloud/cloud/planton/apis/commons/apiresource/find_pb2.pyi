from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FindApiResourcesRequest(_message.Message):
    __slots__ = ("page", "kind", "org", "env")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    page: _pagination_pb2.PageInfo
    kind: _api_resource_kind_pb2.ApiResourceKind
    org: str
    env: str
    def __init__(self, page: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...
