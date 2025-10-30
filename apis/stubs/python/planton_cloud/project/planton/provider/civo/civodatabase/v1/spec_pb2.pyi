from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.civo import region_pb2 as _region_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CivoDatabaseEngine(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    civo_database_engine_unspecified: _ClassVar[CivoDatabaseEngine]
    mysql: _ClassVar[CivoDatabaseEngine]
    postgres: _ClassVar[CivoDatabaseEngine]
civo_database_engine_unspecified: CivoDatabaseEngine
mysql: CivoDatabaseEngine
postgres: CivoDatabaseEngine

class CivoDatabaseSpec(_message.Message):
    __slots__ = ("db_instance_name", "engine", "engine_version", "region", "size_slug", "replicas", "network_id", "firewall_ids", "storage_gib", "tags")
    DB_INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SIZE_SLUG_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    NETWORK_ID_FIELD_NUMBER: _ClassVar[int]
    FIREWALL_IDS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_GIB_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    db_instance_name: str
    engine: CivoDatabaseEngine
    engine_version: str
    region: _region_pb2.CivoRegion
    size_slug: str
    replicas: int
    network_id: _foreign_key_pb2.StringValueOrRef
    firewall_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    storage_gib: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, db_instance_name: _Optional[str] = ..., engine: _Optional[_Union[CivoDatabaseEngine, str]] = ..., engine_version: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.CivoRegion, str]] = ..., size_slug: _Optional[str] = ..., replicas: _Optional[int] = ..., network_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., firewall_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., storage_gib: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...
