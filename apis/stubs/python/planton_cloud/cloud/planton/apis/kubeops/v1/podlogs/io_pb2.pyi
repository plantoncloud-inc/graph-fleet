from cloud.planton.apis.integration.kubernetes.kubernetesobject import io_pb2 as _io_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamKubernetesPodLogsInput(_message.Message):
    __slots__ = ("cloud_resource_id", "options")
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    options: _io_pb2.PodLogStreamOptions
    def __init__(self, cloud_resource_id: _Optional[str] = ..., options: _Optional[_Union[_io_pb2.PodLogStreamOptions, _Mapping]] = ...) -> None: ...
