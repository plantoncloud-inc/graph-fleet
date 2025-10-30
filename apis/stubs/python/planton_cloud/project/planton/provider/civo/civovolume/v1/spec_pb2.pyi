from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.civo import region_pb2 as _region_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CivoVolumeFilesystemType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE: _ClassVar[CivoVolumeFilesystemType]
    EXT4: _ClassVar[CivoVolumeFilesystemType]
    XFS: _ClassVar[CivoVolumeFilesystemType]
NONE: CivoVolumeFilesystemType
EXT4: CivoVolumeFilesystemType
XFS: CivoVolumeFilesystemType

class CivoVolumeSpec(_message.Message):
    __slots__ = ("volume_name", "region", "size_gib", "filesystem_type", "snapshot_id", "tags")
    VOLUME_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SIZE_GIB_FIELD_NUMBER: _ClassVar[int]
    FILESYSTEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_ID_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    volume_name: str
    region: _region_pb2.CivoRegion
    size_gib: int
    filesystem_type: CivoVolumeFilesystemType
    snapshot_id: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, volume_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.CivoRegion, str]] = ..., size_gib: _Optional[int] = ..., filesystem_type: _Optional[_Union[CivoVolumeFilesystemType, str]] = ..., snapshot_id: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
