from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from cloud.planton.apis.connect.terraformbackendcredential.v1 import backend_pb2 as _backend_pb2
from project.planton.shared.iac.terraform import terraform_pb2 as _terraform_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TerraformBackendCredentialSpec(_message.Message):
    __slots__ = ("selector", "type", "s3", "gcs", "azurerm")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    GCS_FIELD_NUMBER: _ClassVar[int]
    AZURERM_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    type: _terraform_pb2.TerraformBackendType
    s3: _backend_pb2.TerraformS3Backend
    gcs: _backend_pb2.TerraformGcsBackend
    azurerm: _backend_pb2.TerraformAzurermBackend
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., type: _Optional[_Union[_terraform_pb2.TerraformBackendType, str]] = ..., s3: _Optional[_Union[_backend_pb2.TerraformS3Backend, _Mapping]] = ..., gcs: _Optional[_Union[_backend_pb2.TerraformGcsBackend, _Mapping]] = ..., azurerm: _Optional[_Union[_backend_pb2.TerraformAzurermBackend, _Mapping]] = ...) -> None: ...
