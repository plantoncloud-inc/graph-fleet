from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TerraformOperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    terraform_operation_type_unspecified: _ClassVar[TerraformOperationType]
    init: _ClassVar[TerraformOperationType]
    refresh: _ClassVar[TerraformOperationType]
    plan: _ClassVar[TerraformOperationType]
    apply: _ClassVar[TerraformOperationType]
    destroy: _ClassVar[TerraformOperationType]

class TerraformBackendType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    terraform_backend_type_unspecified: _ClassVar[TerraformBackendType]
    local: _ClassVar[TerraformBackendType]
    s3: _ClassVar[TerraformBackendType]
    gcs: _ClassVar[TerraformBackendType]
    azurerm: _ClassVar[TerraformBackendType]
terraform_operation_type_unspecified: TerraformOperationType
init: TerraformOperationType
refresh: TerraformOperationType
plan: TerraformOperationType
apply: TerraformOperationType
destroy: TerraformOperationType
terraform_backend_type_unspecified: TerraformBackendType
local: TerraformBackendType
s3: TerraformBackendType
gcs: TerraformBackendType
azurerm: TerraformBackendType
