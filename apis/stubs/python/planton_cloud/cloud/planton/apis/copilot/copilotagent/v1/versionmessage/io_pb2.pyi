from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DraftVersionMessageRequest(_message.Message):
    __slots__ = ("api_resource_kind", "manifest")
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_FIELD_NUMBER: _ClassVar[int]
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    manifest: _any_pb2.Any
    def __init__(self, api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., manifest: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class DraftVersionMessageResponse(_message.Message):
    __slots__ = ("version_message",)
    VERSION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    version_message: str
    def __init__(self, version_message: _Optional[str] = ...) -> None: ...
