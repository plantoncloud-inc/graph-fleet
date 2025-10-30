from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanRegion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    digital_ocean_region_unspecified: _ClassVar[DigitalOceanRegion]
    nyc3: _ClassVar[DigitalOceanRegion]
    sfo3: _ClassVar[DigitalOceanRegion]
    fra1: _ClassVar[DigitalOceanRegion]
    sgp1: _ClassVar[DigitalOceanRegion]
    lon1: _ClassVar[DigitalOceanRegion]
    tor1: _ClassVar[DigitalOceanRegion]
    blr1: _ClassVar[DigitalOceanRegion]
    ams3: _ClassVar[DigitalOceanRegion]
digital_ocean_region_unspecified: DigitalOceanRegion
nyc3: DigitalOceanRegion
sfo3: DigitalOceanRegion
fra1: DigitalOceanRegion
sgp1: DigitalOceanRegion
lon1: DigitalOceanRegion
tor1: DigitalOceanRegion
blr1: DigitalOceanRegion
ams3: DigitalOceanRegion
