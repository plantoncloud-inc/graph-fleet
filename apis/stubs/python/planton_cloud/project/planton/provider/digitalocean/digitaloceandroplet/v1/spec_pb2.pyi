from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanDropletTimezone(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    utc: _ClassVar[DigitalOceanDropletTimezone]
    local: _ClassVar[DigitalOceanDropletTimezone]
utc: DigitalOceanDropletTimezone
local: DigitalOceanDropletTimezone

class DigitalOceanDropletSpec(_message.Message):
    __slots__ = ("droplet_name", "region", "size", "image", "vpc", "enable_ipv6", "enable_backups", "disable_monitoring", "volume_ids", "tags", "user_data", "timezone")
    DROPLET_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    VPC_FIELD_NUMBER: _ClassVar[int]
    ENABLE_IPV6_FIELD_NUMBER: _ClassVar[int]
    ENABLE_BACKUPS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_MONITORING_FIELD_NUMBER: _ClassVar[int]
    VOLUME_IDS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    droplet_name: str
    region: _region_pb2.DigitalOceanRegion
    size: str
    image: str
    vpc: _foreign_key_pb2.StringValueOrRef
    enable_ipv6: bool
    enable_backups: bool
    disable_monitoring: bool
    volume_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    tags: _containers.RepeatedScalarFieldContainer[str]
    user_data: str
    timezone: DigitalOceanDropletTimezone
    def __init__(self, droplet_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., size: _Optional[str] = ..., image: _Optional[str] = ..., vpc: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., enable_ipv6: bool = ..., enable_backups: bool = ..., disable_monitoring: bool = ..., volume_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., tags: _Optional[_Iterable[str]] = ..., user_data: _Optional[str] = ..., timezone: _Optional[_Union[DigitalOceanDropletTimezone, str]] = ...) -> None: ...
