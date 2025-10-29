from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.gcp.gcpdnszone.v1 import spec_pb2 as _spec_pb2
from project.planton.shared.networking.enums.dnsrecordtype import dns_record_type_pb2 as _dns_record_type_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpDnsZoneId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class AddOrUpdateGcpDnsRecordInput(_message.Message):
    __slots__ = ("gcp_dns_zone_id", "record", "version_message")
    GCP_DNS_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    VERSION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    gcp_dns_zone_id: str
    record: _spec_pb2.GcpDnsRecord
    version_message: str
    def __init__(self, gcp_dns_zone_id: _Optional[str] = ..., record: _Optional[_Union[_spec_pb2.GcpDnsRecord, _Mapping]] = ..., version_message: _Optional[str] = ...) -> None: ...

class DeleteGcpDnsRecordInput(_message.Message):
    __slots__ = ("gcp_dns_zone_id", "record_type", "record_name", "version_message")
    GCP_DNS_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    RECORD_TYPE_FIELD_NUMBER: _ClassVar[int]
    RECORD_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    gcp_dns_zone_id: str
    record_type: _dns_record_type_pb2.DnsRecordType
    record_name: str
    version_message: str
    def __init__(self, gcp_dns_zone_id: _Optional[str] = ..., record_type: _Optional[_Union[_dns_record_type_pb2.DnsRecordType, str]] = ..., record_name: _Optional[str] = ..., version_message: _Optional[str] = ...) -> None: ...
