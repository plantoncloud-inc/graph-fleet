from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Probe(_message.Message):
    __slots__ = ("initial_delay_seconds", "period_seconds", "timeout_seconds", "success_threshold", "failure_threshold", "http_get", "grpc", "tcp_socket", "exec")
    INITIAL_DELAY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PERIOD_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    FAILURE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    HTTP_GET_FIELD_NUMBER: _ClassVar[int]
    GRPC_FIELD_NUMBER: _ClassVar[int]
    TCP_SOCKET_FIELD_NUMBER: _ClassVar[int]
    EXEC_FIELD_NUMBER: _ClassVar[int]
    initial_delay_seconds: int
    period_seconds: int
    timeout_seconds: int
    success_threshold: int
    failure_threshold: int
    http_get: HTTPGetAction
    grpc: GRPCAction
    tcp_socket: TCPSocketAction
    exec: ExecAction
    def __init__(self, initial_delay_seconds: _Optional[int] = ..., period_seconds: _Optional[int] = ..., timeout_seconds: _Optional[int] = ..., success_threshold: _Optional[int] = ..., failure_threshold: _Optional[int] = ..., http_get: _Optional[_Union[HTTPGetAction, _Mapping]] = ..., grpc: _Optional[_Union[GRPCAction, _Mapping]] = ..., tcp_socket: _Optional[_Union[TCPSocketAction, _Mapping]] = ..., exec: _Optional[_Union[ExecAction, _Mapping]] = ...) -> None: ...

class HTTPGetAction(_message.Message):
    __slots__ = ("path", "port_number", "port_name", "host", "scheme", "http_headers")
    PATH_FIELD_NUMBER: _ClassVar[int]
    PORT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PORT_NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    HTTP_HEADERS_FIELD_NUMBER: _ClassVar[int]
    path: str
    port_number: int
    port_name: str
    host: str
    scheme: str
    http_headers: _containers.RepeatedCompositeFieldContainer[HTTPHeader]
    def __init__(self, path: _Optional[str] = ..., port_number: _Optional[int] = ..., port_name: _Optional[str] = ..., host: _Optional[str] = ..., scheme: _Optional[str] = ..., http_headers: _Optional[_Iterable[_Union[HTTPHeader, _Mapping]]] = ...) -> None: ...

class HTTPHeader(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class GRPCAction(_message.Message):
    __slots__ = ("port", "service")
    PORT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    port: int
    service: str
    def __init__(self, port: _Optional[int] = ..., service: _Optional[str] = ...) -> None: ...

class TCPSocketAction(_message.Message):
    __slots__ = ("port_number", "port_name", "host")
    PORT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PORT_NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    port_number: int
    port_name: str
    host: str
    def __init__(self, port_number: _Optional[int] = ..., port_name: _Optional[str] = ..., host: _Optional[str] = ...) -> None: ...

class ExecAction(_message.Message):
    __slots__ = ("command",)
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, command: _Optional[_Iterable[str]] = ...) -> None: ...
