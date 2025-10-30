from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanVolumeFilesystemType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE: _ClassVar[DigitalOceanVolumeFilesystemType]
    EXT4: _ClassVar[DigitalOceanVolumeFilesystemType]
    XFS: _ClassVar[DigitalOceanVolumeFilesystemType]
NONE: DigitalOceanVolumeFilesystemType
EXT4: DigitalOceanVolumeFilesystemType
XFS: DigitalOceanVolumeFilesystemType

class DigitalOceanVolumeSpec(_message.Message):
    __slots__ = ("volume_name", "description", "region", "size_gib", "filesystem_type", "snapshot_id", "tags")
    VOLUME_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SIZE_GIB_FIELD_NUMBER: _ClassVar[int]
    FILESYSTEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_ID_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    volume_name: str
    description: str
    region: _region_pb2.DigitalOceanRegion
    size_gib: int
    filesystem_type: DigitalOceanVolumeFilesystemType
    snapshot_id: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, volume_name: _Optional[str] = ..., description: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., size_gib: _Optional[int] = ..., filesystem_type: _Optional[_Union[DigitalOceanVolumeFilesystemType, str]] = ..., snapshot_id: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
