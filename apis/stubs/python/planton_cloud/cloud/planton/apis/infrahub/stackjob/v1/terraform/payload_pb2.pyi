from cloud.planton.apis.infrahub.stackjob.v1.terraform import engine_event_pb2 as _engine_event_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TerraformEngineEventPayload(_message.Message):
    __slots__ = ("diff", "terraform_json_log")
    DIFF_FIELD_NUMBER: _ClassVar[int]
    TERRAFORM_JSON_LOG_FIELD_NUMBER: _ClassVar[int]
    diff: str
    terraform_json_log: _engine_event_pb2.TerraformEngineEventJsonLog
    def __init__(self, diff: _Optional[str] = ..., terraform_json_log: _Optional[_Union[_engine_event_pb2.TerraformEngineEventJsonLog, _Mapping]] = ...) -> None: ...
