from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpCloudCdnSpec(_message.Message):
    __slots__ = ("gcp_project_id",)
    GCP_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    gcp_project_id: str
    def __init__(self, gcp_project_id: _Optional[str] = ...) -> None: ...
