from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadSpecVectorInput(_message.Message):
    __slots__ = ("project_planton_version", "planton_cloud_version", "api_resource_kind")
    PROJECT_PLANTON_VERSION_FIELD_NUMBER: _ClassVar[int]
    PLANTON_CLOUD_VERSION_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    project_planton_version: str
    planton_cloud_version: str
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    def __init__(self, project_planton_version: _Optional[str] = ..., planton_cloud_version: _Optional[str] = ..., api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ...) -> None: ...

class GenerateChatNameRequest(_message.Message):
    __slots__ = ("chat_id",)
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    def __init__(self, chat_id: _Optional[str] = ...) -> None: ...

class GenerateChatNameResponse(_message.Message):
    __slots__ = ("suggested_name",)
    SUGGESTED_NAME_FIELD_NUMBER: _ClassVar[int]
    suggested_name: str
    def __init__(self, suggested_name: _Optional[str] = ...) -> None: ...
