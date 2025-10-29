from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GithubAccountType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    github_account_type_unspecified: _ClassVar[GithubAccountType]
    user: _ClassVar[GithubAccountType]
    organization: _ClassVar[GithubAccountType]
github_account_type_unspecified: GithubAccountType
user: GithubAccountType
organization: GithubAccountType

class GithubCredentialSpec(_message.Message):
    __slots__ = ("github_connection_host", "app_install_info")
    GITHUB_CONNECTION_HOST_FIELD_NUMBER: _ClassVar[int]
    APP_INSTALL_INFO_FIELD_NUMBER: _ClassVar[int]
    github_connection_host: str
    app_install_info: GithubAppInstallInfo
    def __init__(self, github_connection_host: _Optional[str] = ..., app_install_info: _Optional[_Union[GithubAppInstallInfo, _Mapping]] = ...) -> None: ...

class GithubAppInstallInfo(_message.Message):
    __slots__ = ("installation_id", "account_type", "account_id", "account_avatar_url")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    installation_id: int
    account_type: GithubAccountType
    account_id: str
    account_avatar_url: str
    def __init__(self, installation_id: _Optional[int] = ..., account_type: _Optional[_Union[GithubAccountType, str]] = ..., account_id: _Optional[str] = ..., account_avatar_url: _Optional[str] = ...) -> None: ...
