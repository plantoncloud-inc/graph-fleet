from cloud.planton.apis.integration.kubernetes.kubernetesobject import io_pb2 as _io_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecIntoPodContainerInput(_message.Message):
    __slots__ = ("cloud_resource_id", "options")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    options: _io_pb2.PodContainerExecOptions
    def __init__(self, cloud_resource_id: _Optional[str] = ..., options: _Optional[_Union[_io_pb2.PodContainerExecOptions, _Mapping]] = ...) -> None: ...

class BrowserExecIntoPodContainerResponse(_message.Message):
    __slots__ = ("shell_session_id", "command_response")
    SHELL_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    shell_session_id: str
    command_response: _io_pb2.ExecIntoPodContainerResponse
    def __init__(self, shell_session_id: _Optional[str] = ..., command_response: _Optional[_Union[_io_pb2.ExecIntoPodContainerResponse, _Mapping]] = ...) -> None: ...

class BrowserExecuteNextCommandInPodContainerInput(_message.Message):
    __slots__ = ("cloud_resource_id", "shell_session_id", "command")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    SHELL_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    shell_session_id: str
    command: str
    def __init__(self, cloud_resource_id: _Optional[str] = ..., shell_session_id: _Optional[str] = ..., command: _Optional[str] = ...) -> None: ...
