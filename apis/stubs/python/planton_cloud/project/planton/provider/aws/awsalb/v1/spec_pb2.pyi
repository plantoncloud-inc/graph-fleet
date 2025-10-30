from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsAlbSpec(_message.Message):
    __slots__ = ("subnets", "security_groups", "internal", "delete_protection_enabled", "idle_timeout_seconds", "dns", "ssl")
    SUBNETS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUPS_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    DELETE_PROTECTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IDLE_TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DNS_FIELD_NUMBER: _ClassVar[int]
    SSL_FIELD_NUMBER: _ClassVar[int]
    subnets: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    security_groups: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    internal: bool
    delete_protection_enabled: bool
    idle_timeout_seconds: int
    dns: AwsAlbDns
    ssl: AwsAlbSsl
    def __init__(self, subnets: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., security_groups: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., internal: bool = ..., delete_protection_enabled: bool = ..., idle_timeout_seconds: _Optional[int] = ..., dns: _Optional[_Union[AwsAlbDns, _Mapping]] = ..., ssl: _Optional[_Union[AwsAlbSsl, _Mapping]] = ...) -> None: ...

class AwsAlbDns(_message.Message):
    __slots__ = ("enabled", "route53_zone_id", "hostnames")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ROUTE53_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    HOSTNAMES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    route53_zone_id: _foreign_key_pb2.StringValueOrRef
    hostnames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, enabled: bool = ..., route53_zone_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., hostnames: _Optional[_Iterable[str]] = ...) -> None: ...

class AwsAlbSsl(_message.Message):
    __slots__ = ("enabled", "certificate_arn")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_ARN_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    certificate_arn: _foreign_key_pb2.StringValueOrRef
    def __init__(self, enabled: bool = ..., certificate_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ...) -> None: ...
