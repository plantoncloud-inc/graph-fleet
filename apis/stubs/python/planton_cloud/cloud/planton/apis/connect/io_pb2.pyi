from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShareProviderCredentialInput(_message.Message):
    __slots__ = ("provider_credential", "org", "env")
    PROVIDER_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    provider_credential: _selector_pb2.ApiResourceSelector
    org: str
    env: str
    def __init__(self, provider_credential: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...

class UnshareProviderCredentialInput(_message.Message):
    __slots__ = ("provider_credential", "env_id")
    PROVIDER_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    provider_credential: _selector_pb2.ApiResourceSelector
    env_id: str
    def __init__(self, provider_credential: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., env_id: _Optional[str] = ...) -> None: ...
