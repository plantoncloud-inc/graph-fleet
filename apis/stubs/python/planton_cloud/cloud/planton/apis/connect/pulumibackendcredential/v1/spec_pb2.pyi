from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from cloud.planton.apis.connect.pulumibackendcredential.v1 import backend_pb2 as _backend_pb2
from project.planton.shared.iac.pulumi import pulumi_pb2 as _pulumi_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PulumiBackendCredentialSpec(_message.Message):
    __slots__ = ("selector", "type", "http", "s3", "gcs", "azurerm")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HTTP_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    GCS_FIELD_NUMBER: _ClassVar[int]
    AZURERM_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    type: _pulumi_pb2.PulumiBackendType
    http: _backend_pb2.PulumiHttpBackend
    s3: _backend_pb2.PulumiS3Backend
    gcs: _backend_pb2.PulumiGcsBackend
    azurerm: _backend_pb2.PulumiAzurermBackend
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., type: _Optional[_Union[_pulumi_pb2.PulumiBackendType, str]] = ..., http: _Optional[_Union[_backend_pb2.PulumiHttpBackend, _Mapping]] = ..., s3: _Optional[_Union[_backend_pb2.PulumiS3Backend, _Mapping]] = ..., gcs: _Optional[_Union[_backend_pb2.PulumiGcsBackend, _Mapping]] = ..., azurerm: _Optional[_Union[_backend_pb2.PulumiAzurermBackend, _Mapping]] = ...) -> None: ...
