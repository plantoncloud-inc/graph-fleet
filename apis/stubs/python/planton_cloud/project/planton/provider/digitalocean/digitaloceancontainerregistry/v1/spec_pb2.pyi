from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanContainerRegistryTier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    digitalocean_container_registry_tier_unspecified: _ClassVar[DigitalOceanContainerRegistryTier]
    STARTER: _ClassVar[DigitalOceanContainerRegistryTier]
    BASIC: _ClassVar[DigitalOceanContainerRegistryTier]
    PROFESSIONAL: _ClassVar[DigitalOceanContainerRegistryTier]
digitalocean_container_registry_tier_unspecified: DigitalOceanContainerRegistryTier
STARTER: DigitalOceanContainerRegistryTier
BASIC: DigitalOceanContainerRegistryTier
PROFESSIONAL: DigitalOceanContainerRegistryTier

class DigitalOceanContainerRegistrySpec(_message.Message):
    __slots__ = ("name", "subscription_tier", "region", "garbage_collection_enabled")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_TIER_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    GARBAGE_COLLECTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    name: str
    subscription_tier: DigitalOceanContainerRegistryTier
    region: _region_pb2.DigitalOceanRegion
    garbage_collection_enabled: bool
    def __init__(self, name: _Optional[str] = ..., subscription_tier: _Optional[_Union[DigitalOceanContainerRegistryTier, str]] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., garbage_collection_enabled: bool = ...) -> None: ...
