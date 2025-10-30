from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanFunctionRuntime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    digital_ocean_function_runtime_unspecified: _ClassVar[DigitalOceanFunctionRuntime]
    nodejs: _ClassVar[DigitalOceanFunctionRuntime]
    python: _ClassVar[DigitalOceanFunctionRuntime]
    go: _ClassVar[DigitalOceanFunctionRuntime]
    rust: _ClassVar[DigitalOceanFunctionRuntime]
    deno: _ClassVar[DigitalOceanFunctionRuntime]
digital_ocean_function_runtime_unspecified: DigitalOceanFunctionRuntime
nodejs: DigitalOceanFunctionRuntime
python: DigitalOceanFunctionRuntime
go: DigitalOceanFunctionRuntime
rust: DigitalOceanFunctionRuntime
deno: DigitalOceanFunctionRuntime

class DigitalOceanFunctionSpec(_message.Message):
    __slots__ = ("function_name", "region", "runtime", "entrypoint", "memory_mb", "timeout_seconds", "env")
    class EnvEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    ENTRYPOINT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    region: _region_pb2.DigitalOceanRegion
    runtime: DigitalOceanFunctionRuntime
    entrypoint: str
    memory_mb: int
    timeout_seconds: int
    env: _containers.ScalarMap[str, str]
    def __init__(self, function_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., runtime: _Optional[_Union[DigitalOceanFunctionRuntime, str]] = ..., entrypoint: _Optional[str] = ..., memory_mb: _Optional[int] = ..., timeout_seconds: _Optional[int] = ..., env: _Optional[_Mapping[str, str]] = ...) -> None: ...
