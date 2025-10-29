from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class TerraformEngineOperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    terraform_engine_operation_type_unspecified: _ClassVar[TerraformEngineOperationType]
    noop: _ClassVar[TerraformEngineOperationType]
    create: _ClassVar[TerraformEngineOperationType]
    read: _ClassVar[TerraformEngineOperationType]
    update: _ClassVar[TerraformEngineOperationType]
    delete: _ClassVar[TerraformEngineOperationType]
    replace: _ClassVar[TerraformEngineOperationType]
    move: _ClassVar[TerraformEngineOperationType]
    change_action_import: _ClassVar[TerraformEngineOperationType]
    remove: _ClassVar[TerraformEngineOperationType]
    refresh: _ClassVar[TerraformEngineOperationType]

class TerraformEngineEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    terraform_engine_event_type_unspecified: _ClassVar[TerraformEngineEventType]
    plan_start: _ClassVar[TerraformEngineEventType]
    plan_complete: _ClassVar[TerraformEngineEventType]
    plan_errored: _ClassVar[TerraformEngineEventType]
    apply_start: _ClassVar[TerraformEngineEventType]
    apply_complete: _ClassVar[TerraformEngineEventType]
    apply_errored: _ClassVar[TerraformEngineEventType]
    refresh_start: _ClassVar[TerraformEngineEventType]
    refresh_complete: _ClassVar[TerraformEngineEventType]
    refresh_errored: _ClassVar[TerraformEngineEventType]
    cost_estimate_start: _ClassVar[TerraformEngineEventType]
    cost_estimate_complete: _ClassVar[TerraformEngineEventType]
    cost_estimate_errored: _ClassVar[TerraformEngineEventType]
    destroy_start: _ClassVar[TerraformEngineEventType]
    destroy_complete: _ClassVar[TerraformEngineEventType]
    destroy_errored: _ClassVar[TerraformEngineEventType]
    step: _ClassVar[TerraformEngineEventType]
    version: _ClassVar[TerraformEngineEventType]
    diagnostic: _ClassVar[TerraformEngineEventType]
    output: _ClassVar[TerraformEngineEventType]
    log: _ClassVar[TerraformEngineEventType]
    planned_change: _ClassVar[TerraformEngineEventType]
    change_summary: _ClassVar[TerraformEngineEventType]
    apply_progress: _ClassVar[TerraformEngineEventType]
    resource_drift: _ClassVar[TerraformEngineEventType]
    outputs: _ClassVar[TerraformEngineEventType]
terraform_engine_operation_type_unspecified: TerraformEngineOperationType
noop: TerraformEngineOperationType
create: TerraformEngineOperationType
read: TerraformEngineOperationType
update: TerraformEngineOperationType
delete: TerraformEngineOperationType
replace: TerraformEngineOperationType
move: TerraformEngineOperationType
change_action_import: TerraformEngineOperationType
remove: TerraformEngineOperationType
refresh: TerraformEngineOperationType
terraform_engine_event_type_unspecified: TerraformEngineEventType
plan_start: TerraformEngineEventType
plan_complete: TerraformEngineEventType
plan_errored: TerraformEngineEventType
apply_start: TerraformEngineEventType
apply_complete: TerraformEngineEventType
apply_errored: TerraformEngineEventType
refresh_start: TerraformEngineEventType
refresh_complete: TerraformEngineEventType
refresh_errored: TerraformEngineEventType
cost_estimate_start: TerraformEngineEventType
cost_estimate_complete: TerraformEngineEventType
cost_estimate_errored: TerraformEngineEventType
destroy_start: TerraformEngineEventType
destroy_complete: TerraformEngineEventType
destroy_errored: TerraformEngineEventType
step: TerraformEngineEventType
version: TerraformEngineEventType
diagnostic: TerraformEngineEventType
output: TerraformEngineEventType
log: TerraformEngineEventType
planned_change: TerraformEngineEventType
change_summary: TerraformEngineEventType
apply_progress: TerraformEngineEventType
resource_drift: TerraformEngineEventType
outputs: TerraformEngineEventType
