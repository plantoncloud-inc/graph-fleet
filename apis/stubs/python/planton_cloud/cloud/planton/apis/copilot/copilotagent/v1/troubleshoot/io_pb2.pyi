from cloud.planton.apis.servicehub.pipeline.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.servicehub.service.v1 import api_pb2 as _api_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TroubleshootImageBuildRequest(_message.Message):
    __slots__ = ("service", "pipeline", "image_build_log")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BUILD_LOG_FIELD_NUMBER: _ClassVar[int]
    service: _api_pb2_1.Service
    pipeline: _api_pb2.Pipeline
    image_build_log: str
    def __init__(self, service: _Optional[_Union[_api_pb2_1.Service, _Mapping]] = ..., pipeline: _Optional[_Union[_api_pb2.Pipeline, _Mapping]] = ..., image_build_log: _Optional[str] = ...) -> None: ...

class TroubleshootImageBuildResponse(_message.Message):
    __slots__ = ("solution",)
    SOLUTION_FIELD_NUMBER: _ClassVar[int]
    solution: str
    def __init__(self, solution: _Optional[str] = ...) -> None: ...
