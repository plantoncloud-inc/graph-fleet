from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEcsClusterSpec(_message.Message):
    __slots__ = ("enable_container_insights", "capacity_providers", "enable_execute_command")
    ENABLE_CONTAINER_INSIGHTS_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_EXECUTE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    enable_container_insights: bool
    capacity_providers: _containers.RepeatedScalarFieldContainer[str]
    enable_execute_command: bool
    def __init__(self, enable_container_insights: bool = ..., capacity_providers: _Optional[_Iterable[str]] = ..., enable_execute_command: bool = ...) -> None: ...
