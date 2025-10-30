from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class DnsRecordType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    unspecified: _ClassVar[DnsRecordType]
    A: _ClassVar[DnsRecordType]
    AAAA: _ClassVar[DnsRecordType]
    ALIAS: _ClassVar[DnsRecordType]
    CNAME: _ClassVar[DnsRecordType]
    MX: _ClassVar[DnsRecordType]
    NS: _ClassVar[DnsRecordType]
    PTR: _ClassVar[DnsRecordType]
    SOA: _ClassVar[DnsRecordType]
    SRV: _ClassVar[DnsRecordType]
    TXT: _ClassVar[DnsRecordType]
unspecified: DnsRecordType
A: DnsRecordType
AAAA: DnsRecordType
ALIAS: DnsRecordType
CNAME: DnsRecordType
MX: DnsRecordType
NS: DnsRecordType
PTR: DnsRecordType
SOA: DnsRecordType
SRV: DnsRecordType
TXT: DnsRecordType
