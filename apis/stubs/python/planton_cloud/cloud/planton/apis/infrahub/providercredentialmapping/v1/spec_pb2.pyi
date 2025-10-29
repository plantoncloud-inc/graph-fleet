from cloud.planton.apis.commons.apiresource import io_pb2 as _io_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProviderCredentialMappingSpec(_message.Message):
    __slots__ = ("selector", "provider_credential")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    provider_credential: _io_pb2.ApiResourceKindAndNameAndId
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., provider_credential: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ...) -> None: ...
