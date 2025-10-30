from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanBucketAccessControl(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRIVATE: _ClassVar[DigitalOceanBucketAccessControl]
    PUBLIC_READ: _ClassVar[DigitalOceanBucketAccessControl]
PRIVATE: DigitalOceanBucketAccessControl
PUBLIC_READ: DigitalOceanBucketAccessControl

class DigitalOceanBucketSpec(_message.Message):
    __slots__ = ("bucket_name", "region", "access_control", "versioning_enabled", "tags")
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ACCESS_CONTROL_FIELD_NUMBER: _ClassVar[int]
    VERSIONING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    bucket_name: str
    region: _region_pb2.DigitalOceanRegion
    access_control: DigitalOceanBucketAccessControl
    versioning_enabled: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, bucket_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., access_control: _Optional[_Union[DigitalOceanBucketAccessControl, str]] = ..., versioning_enabled: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
