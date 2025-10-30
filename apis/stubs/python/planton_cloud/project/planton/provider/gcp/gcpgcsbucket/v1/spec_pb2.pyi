from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGcsBucketSpec(_message.Message):
    __slots__ = ("gcp_project_id", "gcp_region", "is_public")
    GCP_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    GCP_REGION_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    gcp_project_id: str
    gcp_region: str
    is_public: bool
    def __init__(self, gcp_project_id: _Optional[str] = ..., gcp_region: _Optional[str] = ..., is_public: bool = ...) -> None: ...
