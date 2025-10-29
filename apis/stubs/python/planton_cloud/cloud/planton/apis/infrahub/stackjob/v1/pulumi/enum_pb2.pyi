from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class PulumiEngineOperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    pulumi_engine_operation_type_unspecified: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_SAME: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_CREATE: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_UPDATE: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_DELETE: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_REPLACE: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_CREATE_REPLACEMENT: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_DELETE_REPLACED: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_READ: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_READ_REPLACEMENT: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_REFRESH: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_READ_DISCARD: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_DISCARD_REPLACED: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_REMOVE_PENDING_REPLACE: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_IMPORT: _ClassVar[PulumiEngineOperationType]
    OP_TYPE_IMPORT_REPLACEMENT: _ClassVar[PulumiEngineOperationType]

class PulumiEngineEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    pulumi_engine_event_type_unspecified: _ClassVar[PulumiEngineEventType]
    CANCEL: _ClassVar[PulumiEngineEventType]
    STDOUT: _ClassVar[PulumiEngineEventType]
    DIAGNOSTIC: _ClassVar[PulumiEngineEventType]
    PRELUDE: _ClassVar[PulumiEngineEventType]
    SUMMARY: _ClassVar[PulumiEngineEventType]
    RESOURCE_PRE: _ClassVar[PulumiEngineEventType]
    RES_OUTPUTS: _ClassVar[PulumiEngineEventType]
    RES_OP_FAILED: _ClassVar[PulumiEngineEventType]
    POLICY: _ClassVar[PulumiEngineEventType]
    POLICY_REMEDIATION: _ClassVar[PulumiEngineEventType]
pulumi_engine_operation_type_unspecified: PulumiEngineOperationType
OP_TYPE_SAME: PulumiEngineOperationType
OP_TYPE_CREATE: PulumiEngineOperationType
OP_TYPE_UPDATE: PulumiEngineOperationType
OP_TYPE_DELETE: PulumiEngineOperationType
OP_TYPE_REPLACE: PulumiEngineOperationType
OP_TYPE_CREATE_REPLACEMENT: PulumiEngineOperationType
OP_TYPE_DELETE_REPLACED: PulumiEngineOperationType
OP_TYPE_READ: PulumiEngineOperationType
OP_TYPE_READ_REPLACEMENT: PulumiEngineOperationType
OP_TYPE_REFRESH: PulumiEngineOperationType
OP_TYPE_READ_DISCARD: PulumiEngineOperationType
OP_TYPE_DISCARD_REPLACED: PulumiEngineOperationType
OP_TYPE_REMOVE_PENDING_REPLACE: PulumiEngineOperationType
OP_TYPE_IMPORT: PulumiEngineOperationType
OP_TYPE_IMPORT_REPLACEMENT: PulumiEngineOperationType
pulumi_engine_event_type_unspecified: PulumiEngineEventType
CANCEL: PulumiEngineEventType
STDOUT: PulumiEngineEventType
DIAGNOSTIC: PulumiEngineEventType
PRELUDE: PulumiEngineEventType
SUMMARY: PulumiEngineEventType
RESOURCE_PRE: PulumiEngineEventType
RES_OUTPUTS: PulumiEngineEventType
RES_OP_FAILED: PulumiEngineEventType
POLICY: PulumiEngineEventType
POLICY_REMEDIATION: PulumiEngineEventType
