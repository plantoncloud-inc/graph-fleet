from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from cloud.planton.apis.infrahub.providercredentialmapping.v1 import api_pb2 as _api_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetProviderCredentialMappingBySelectorInput(_message.Message):
    __slots__ = ("selector", "provider_credential_kind")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CREDENTIAL_KIND_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    provider_credential_kind: _api_resource_kind_pb2.ApiResourceKind
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., provider_credential_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ...) -> None: ...

class ProviderCredentialMappings(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.ProviderCredentialMapping]
    def __init__(self, entries: _Optional[_Iterable[_Union[_api_pb2.ProviderCredentialMapping, _Mapping]]] = ...) -> None: ...
