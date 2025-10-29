from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiDocsFieldSearchRecord(_message.Message):
    __slots__ = ("id", "kind", "message_name", "message_full_name", "field_type", "field_name", "field_description", "field_path")
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
    FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FIELD_PATH_FIELD_NUMBER: _ClassVar[int]
    id: str
    kind: _api_resource_kind_pb2.ApiResourceKind
    message_name: str
    message_full_name: str
    field_type: str
    field_name: str
    field_description: str
    field_path: str
    def __init__(self, id: _Optional[str] = ..., kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., message_name: _Optional[str] = ..., message_full_name: _Optional[str] = ..., field_type: _Optional[str] = ..., field_name: _Optional[str] = ..., field_description: _Optional[str] = ..., field_path: _Optional[str] = ...) -> None: ...

class HelpTextFieldMap(_message.Message):
    __slots__ = ("field_map",)
    class FieldMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FIELD_MAP_FIELD_NUMBER: _ClassVar[int]
    field_map: _containers.ScalarMap[str, str]
    def __init__(self, field_map: _Optional[_Mapping[str, str]] = ...) -> None: ...

class IndexApiDocsRequest(_message.Message):
    __slots__ = ("api_docs_json", "apis_version")
    API_DOCS_JSON_FIELD_NUMBER: _ClassVar[int]
    APIS_VERSION_FIELD_NUMBER: _ClassVar[int]
    ASYNC_FIELD_NUMBER: _ClassVar[int]
    api_docs_json: str
    apis_version: str
    def __init__(self, api_docs_json: _Optional[str] = ..., apis_version: _Optional[str] = ..., **kwargs) -> None: ...

class IndexApiDocsProgressResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
