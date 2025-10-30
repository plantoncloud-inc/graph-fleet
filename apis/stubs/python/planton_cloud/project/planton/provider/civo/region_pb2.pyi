from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class CivoRegion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    civo_region_unspecified: _ClassVar[CivoRegion]
    lon1: _ClassVar[CivoRegion]
    lon2: _ClassVar[CivoRegion]
    fra1: _ClassVar[CivoRegion]
    nyc1: _ClassVar[CivoRegion]
    phx1: _ClassVar[CivoRegion]
    mum1: _ClassVar[CivoRegion]
civo_region_unspecified: CivoRegion
lon1: CivoRegion
lon2: CivoRegion
fra1: CivoRegion
nyc1: CivoRegion
phx1: CivoRegion
mum1: CivoRegion
