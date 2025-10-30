from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareDnsZonePlan(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FREE: _ClassVar[CloudflareDnsZonePlan]
    PRO: _ClassVar[CloudflareDnsZonePlan]
    BUSINESS: _ClassVar[CloudflareDnsZonePlan]
    ENTERPRISE: _ClassVar[CloudflareDnsZonePlan]
FREE: CloudflareDnsZonePlan
PRO: CloudflareDnsZonePlan
BUSINESS: CloudflareDnsZonePlan
ENTERPRISE: CloudflareDnsZonePlan

class CloudflareDnsZoneSpec(_message.Message):
    __slots__ = ("zone_name", "account_id", "plan", "paused", "default_proxied")
    ZONE_NAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PROXIED_FIELD_NUMBER: _ClassVar[int]
    zone_name: str
    account_id: str
    plan: CloudflareDnsZonePlan
    paused: bool
    default_proxied: bool
    def __init__(self, zone_name: _Optional[str] = ..., account_id: _Optional[str] = ..., plan: _Optional[_Union[CloudflareDnsZonePlan, str]] = ..., paused: bool = ..., default_proxied: bool = ...) -> None: ...
