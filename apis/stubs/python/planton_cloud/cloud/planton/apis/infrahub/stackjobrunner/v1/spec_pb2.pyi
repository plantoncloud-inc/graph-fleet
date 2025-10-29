from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StackJobRunnerSpec(_message.Message):
    __slots__ = ("selector", "connection")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    connection: StackJobRunnerConnection
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., connection: _Optional[_Union[StackJobRunnerConnection, _Mapping]] = ...) -> None: ...

class StackJobRunnerConnection(_message.Message):
    __slots__ = ("grpc_endpoint", "use_secure_connection", "grpc_metadata")
    class GrpcMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    GRPC_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    USE_SECURE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    GRPC_METADATA_FIELD_NUMBER: _ClassVar[int]
    grpc_endpoint: str
    use_secure_connection: bool
    grpc_metadata: _containers.ScalarMap[str, str]
    def __init__(self, grpc_endpoint: _Optional[str] = ..., use_secure_connection: bool = ..., grpc_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...
