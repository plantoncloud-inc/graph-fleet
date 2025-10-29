from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.networking.enums.dnsrecordtype import dns_record_type_pb2 as _dns_record_type_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CivoDnsZoneSpec(_message.Message):
    __slots__ = ("domain_name", "records")
    DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    domain_name: str
    records: _containers.RepeatedCompositeFieldContainer[CivoDnsZoneRecord]
    def __init__(self, domain_name: _Optional[str] = ..., records: _Optional[_Iterable[_Union[CivoDnsZoneRecord, _Mapping]]] = ...) -> None: ...

class CivoDnsZoneRecord(_message.Message):
    __slots__ = ("name", "values", "ttl_seconds", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    values: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    ttl_seconds: int
    type: _dns_record_type_pb2.DnsRecordType
    def __init__(self, name: _Optional[str] = ..., values: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., ttl_seconds: _Optional[int] = ..., type: _Optional[_Union[_dns_record_type_pb2.DnsRecordType, str]] = ...) -> None: ...
