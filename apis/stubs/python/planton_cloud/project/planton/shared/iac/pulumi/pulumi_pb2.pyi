from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class PulumiOperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    pulumi_operation_type_unspecified: _ClassVar[PulumiOperationType]
    refresh: _ClassVar[PulumiOperationType]
    update: _ClassVar[PulumiOperationType]
    destroy: _ClassVar[PulumiOperationType]

class PulumiBackendType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    type_unspecified: _ClassVar[PulumiBackendType]
    http: _ClassVar[PulumiBackendType]
    s3: _ClassVar[PulumiBackendType]
    gcs: _ClassVar[PulumiBackendType]
    azurerm: _ClassVar[PulumiBackendType]
pulumi_operation_type_unspecified: PulumiOperationType
refresh: PulumiOperationType
update: PulumiOperationType
destroy: PulumiOperationType
type_unspecified: PulumiBackendType
http: PulumiBackendType
s3: PulumiBackendType
gcs: PulumiBackendType
azurerm: PulumiBackendType
