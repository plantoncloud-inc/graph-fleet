from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanDatabaseEngine(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    digital_ocean_database_engine_unspecified: _ClassVar[DigitalOceanDatabaseEngine]
    postgres: _ClassVar[DigitalOceanDatabaseEngine]
    mysql: _ClassVar[DigitalOceanDatabaseEngine]
    redis: _ClassVar[DigitalOceanDatabaseEngine]
    mongodb: _ClassVar[DigitalOceanDatabaseEngine]
digital_ocean_database_engine_unspecified: DigitalOceanDatabaseEngine
postgres: DigitalOceanDatabaseEngine
mysql: DigitalOceanDatabaseEngine
redis: DigitalOceanDatabaseEngine
mongodb: DigitalOceanDatabaseEngine

class DigitalOceanDatabaseClusterSpec(_message.Message):
    __slots__ = ("cluster_name", "engine", "engine_version", "region", "size_slug", "node_count", "vpc", "storage_gib", "enable_public_connectivity")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SIZE_SLUG_FIELD_NUMBER: _ClassVar[int]
    NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    VPC_FIELD_NUMBER: _ClassVar[int]
    STORAGE_GIB_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PUBLIC_CONNECTIVITY_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    engine: DigitalOceanDatabaseEngine
    engine_version: str
    region: _region_pb2.DigitalOceanRegion
    size_slug: str
    node_count: int
    vpc: _foreign_key_pb2.StringValueOrRef
    storage_gib: int
    enable_public_connectivity: bool
    def __init__(self, cluster_name: _Optional[str] = ..., engine: _Optional[_Union[DigitalOceanDatabaseEngine, str]] = ..., engine_version: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., size_slug: _Optional[str] = ..., node_count: _Optional[int] = ..., vpc: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., storage_gib: _Optional[int] = ..., enable_public_connectivity: bool = ...) -> None: ...
