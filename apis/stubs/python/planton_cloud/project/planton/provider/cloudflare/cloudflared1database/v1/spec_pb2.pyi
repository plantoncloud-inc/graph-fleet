from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareD1Region(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    cloudflare_d1_region_unspecified: _ClassVar[CloudflareD1Region]
    weur: _ClassVar[CloudflareD1Region]
    enw: _ClassVar[CloudflareD1Region]
    ape: _ClassVar[CloudflareD1Region]
    usw: _ClassVar[CloudflareD1Region]
cloudflare_d1_region_unspecified: CloudflareD1Region
weur: CloudflareD1Region
enw: CloudflareD1Region
ape: CloudflareD1Region
usw: CloudflareD1Region

class CloudflareD1DatabaseSpec(_message.Message):
    __slots__ = ("database_name", "account_id", "region", "primary_key", "preview_branch")
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_KEY_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_BRANCH_FIELD_NUMBER: _ClassVar[int]
    database_name: str
    account_id: str
    region: CloudflareD1Region
    primary_key: str
    preview_branch: bool
    def __init__(self, database_name: _Optional[str] = ..., account_id: _Optional[str] = ..., region: _Optional[_Union[CloudflareD1Region, str]] = ..., primary_key: _Optional[str] = ..., preview_branch: bool = ...) -> None: ...
