from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.civo import region_pb2 as _region_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CivoBucketSpec(_message.Message):
    __slots__ = ("bucket_name", "region", "versioning_enabled", "tags")
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    VERSIONING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    bucket_name: str
    region: _region_pb2.CivoRegion
    versioning_enabled: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, bucket_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.CivoRegion, str]] = ..., versioning_enabled: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
