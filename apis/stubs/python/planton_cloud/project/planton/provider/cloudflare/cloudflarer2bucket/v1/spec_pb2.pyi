from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareR2Location(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUDFLARE_R2_LOCATION_UNSPECIFIED: _ClassVar[CloudflareR2Location]
    WNAM: _ClassVar[CloudflareR2Location]
    ENAM: _ClassVar[CloudflareR2Location]
    WEUR: _ClassVar[CloudflareR2Location]
    EEUR: _ClassVar[CloudflareR2Location]
    APAC: _ClassVar[CloudflareR2Location]
    OC: _ClassVar[CloudflareR2Location]
CLOUDFLARE_R2_LOCATION_UNSPECIFIED: CloudflareR2Location
WNAM: CloudflareR2Location
ENAM: CloudflareR2Location
WEUR: CloudflareR2Location
EEUR: CloudflareR2Location
APAC: CloudflareR2Location
OC: CloudflareR2Location

class CloudflareR2BucketSpec(_message.Message):
    __slots__ = ("bucket_name", "account_id", "location", "public_access", "versioning_enabled")
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_ACCESS_FIELD_NUMBER: _ClassVar[int]
    VERSIONING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    bucket_name: str
    account_id: str
    location: CloudflareR2Location
    public_access: bool
    versioning_enabled: bool
    def __init__(self, bucket_name: _Optional[str] = ..., account_id: _Optional[str] = ..., location: _Optional[_Union[CloudflareR2Location, str]] = ..., public_access: bool = ..., versioning_enabled: bool = ...) -> None: ...
