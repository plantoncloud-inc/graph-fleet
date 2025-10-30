from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.networking.enums.dnsrecordtype import dns_record_type_pb2 as _dns_record_type_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpDnsZoneSpec(_message.Message):
    __slots__ = ("project_id", "iam_service_accounts", "records")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    IAM_SERVICE_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    iam_service_accounts: _containers.RepeatedScalarFieldContainer[str]
    records: _containers.RepeatedCompositeFieldContainer[GcpDnsRecord]
    def __init__(self, project_id: _Optional[str] = ..., iam_service_accounts: _Optional[_Iterable[str]] = ..., records: _Optional[_Iterable[_Union[GcpDnsRecord, _Mapping]]] = ...) -> None: ...

class GcpDnsRecord(_message.Message):
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
