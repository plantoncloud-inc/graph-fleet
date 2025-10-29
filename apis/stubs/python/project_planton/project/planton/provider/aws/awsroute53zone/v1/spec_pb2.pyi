from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.networking.enums.dnsrecordtype import dns_record_type_pb2 as _dns_record_type_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsRoute53ZoneSpec(_message.Message):
    __slots__ = ("records",)
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[Route53DnsRecord]
    def __init__(self, records: _Optional[_Iterable[_Union[Route53DnsRecord, _Mapping]]] = ...) -> None: ...

class Route53DnsRecord(_message.Message):
    __slots__ = ("record_type", "name", "values", "ttl_seconds")
    RECORD_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    record_type: _dns_record_type_pb2.DnsRecordType
    name: str
    values: _containers.RepeatedScalarFieldContainer[str]
    ttl_seconds: int
    def __init__(self, record_type: _Optional[_Union[_dns_record_type_pb2.DnsRecordType, str]] = ..., name: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ..., ttl_seconds: _Optional[int] = ...) -> None: ...
