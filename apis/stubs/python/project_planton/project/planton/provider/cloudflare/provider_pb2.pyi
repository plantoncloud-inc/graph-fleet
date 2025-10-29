from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareAuthScheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    cloudflare_auth_scheme_unspecified: _ClassVar[CloudflareAuthScheme]
    api_token: _ClassVar[CloudflareAuthScheme]
    legacy_api_key: _ClassVar[CloudflareAuthScheme]
cloudflare_auth_scheme_unspecified: CloudflareAuthScheme
api_token: CloudflareAuthScheme
legacy_api_key: CloudflareAuthScheme

class CloudflareProviderConfig(_message.Message):
    __slots__ = ("auth_scheme", "api_token", "api_key", "email", "r2")
    AUTH_SCHEME_FIELD_NUMBER: _ClassVar[int]
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    R2_FIELD_NUMBER: _ClassVar[int]
    auth_scheme: CloudflareAuthScheme
    api_token: str
    api_key: str
    email: str
    r2: CloudflareCredentialsR2Spec
    def __init__(self, auth_scheme: _Optional[_Union[CloudflareAuthScheme, str]] = ..., api_token: _Optional[str] = ..., api_key: _Optional[str] = ..., email: _Optional[str] = ..., r2: _Optional[_Union[CloudflareCredentialsR2Spec, _Mapping]] = ...) -> None: ...

class CloudflareCredentialsR2Spec(_message.Message):
    __slots__ = ("access_key_id", "secret_access_key", "endpoint")
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    access_key_id: str
    secret_access_key: str
    endpoint: str
    def __init__(self, access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ..., endpoint: _Optional[str] = ...) -> None: ...
