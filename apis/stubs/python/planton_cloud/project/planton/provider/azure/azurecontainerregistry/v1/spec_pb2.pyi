from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AzureContainerRegistrySku(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BASIC: _ClassVar[AzureContainerRegistrySku]
    STANDARD: _ClassVar[AzureContainerRegistrySku]
    PREMIUM: _ClassVar[AzureContainerRegistrySku]
BASIC: AzureContainerRegistrySku
STANDARD: AzureContainerRegistrySku
PREMIUM: AzureContainerRegistrySku

class AzureContainerRegistrySpec(_message.Message):
    __slots__ = ("registry_name", "sku", "admin_user_enabled", "geo_replication_regions")
    REGISTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    SKU_FIELD_NUMBER: _ClassVar[int]
    ADMIN_USER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    GEO_REPLICATION_REGIONS_FIELD_NUMBER: _ClassVar[int]
    registry_name: str
    sku: AzureContainerRegistrySku
    admin_user_enabled: bool
    geo_replication_regions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, registry_name: _Optional[str] = ..., sku: _Optional[_Union[AzureContainerRegistrySku, str]] = ..., admin_user_enabled: bool = ..., geo_replication_regions: _Optional[_Iterable[str]] = ...) -> None: ...
