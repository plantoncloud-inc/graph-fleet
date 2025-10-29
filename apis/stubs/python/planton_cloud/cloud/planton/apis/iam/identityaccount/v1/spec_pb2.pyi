from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from cloud.planton.apis.iam.identityaccount.v1 import enums_pb2 as _enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IdentityAccountSpec(_message.Message):
    __slots__ = ("identity_account_type", "idp_id", "email", "first_name", "last_name", "picture_url", "github_username")
    IDENTITY_ACCOUNT_TYPE_FIELD_NUMBER: _ClassVar[int]
    IDP_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    GITHUB_USERNAME_FIELD_NUMBER: _ClassVar[int]
    identity_account_type: _enums_pb2.IdentityAccountType
    idp_id: str
    email: str
    first_name: str
    last_name: str
    picture_url: str
    github_username: str
    def __init__(self, identity_account_type: _Optional[_Union[_enums_pb2.IdentityAccountType, str]] = ..., idp_id: _Optional[str] = ..., email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., picture_url: _Optional[str] = ..., github_username: _Optional[str] = ...) -> None: ...
