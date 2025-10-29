from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class StackJobOperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    stack_job_operation_type_unspecified: _ClassVar[StackJobOperationType]
    init: _ClassVar[StackJobOperationType]
    refresh: _ClassVar[StackJobOperationType]
    update_preview: _ClassVar[StackJobOperationType]
    update: _ClassVar[StackJobOperationType]
    destroy_preview: _ClassVar[StackJobOperationType]
    destroy: _ClassVar[StackJobOperationType]

class StackJobProgressEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    stack_job_progress_event_type_unspecified: _ClassVar[StackJobProgressEventType]
    stack_job_status_changed_event: _ClassVar[StackJobProgressEventType]
    iac_module_repo_setup_event: _ClassVar[StackJobProgressEventType]
    iac_operation_status_event: _ClassVar[StackJobProgressEventType]
    iac_stack_resources_event: _ClassVar[StackJobProgressEventType]
    iac_stack_outputs_event: _ClassVar[StackJobProgressEventType]
    terraform_engine_event: _ClassVar[StackJobProgressEventType]
    pulumi_engine_event: _ClassVar[StackJobProgressEventType]

class IacResourceProgressStatusLabel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    iac_resource_progress_status_label_unspecified: _ClassVar[IacResourceProgressStatusLabel]
    refreshing: _ClassVar[IacResourceProgressStatusLabel]
    unchanged: _ClassVar[IacResourceProgressStatusLabel]
    create: _ClassVar[IacResourceProgressStatusLabel]
    iac_resource_progress_status_label_update: _ClassVar[IacResourceProgressStatusLabel]
    delete: _ClassVar[IacResourceProgressStatusLabel]
    replace: _ClassVar[IacResourceProgressStatusLabel]
    creating: _ClassVar[IacResourceProgressStatusLabel]
    updating: _ClassVar[IacResourceProgressStatusLabel]
    deleting: _ClassVar[IacResourceProgressStatusLabel]
    replacing: _ClassVar[IacResourceProgressStatusLabel]
    refreshed: _ClassVar[IacResourceProgressStatusLabel]
    iac_resource_progress_status_label_created: _ClassVar[IacResourceProgressStatusLabel]
    iac_resource_progress_status_label_updated: _ClassVar[IacResourceProgressStatusLabel]
    iac_resource_progress_status_label_deleted: _ClassVar[IacResourceProgressStatusLabel]
    replaced: _ClassVar[IacResourceProgressStatusLabel]
    refresh_failed: _ClassVar[IacResourceProgressStatusLabel]
    create_failed: _ClassVar[IacResourceProgressStatusLabel]
    update_failed: _ClassVar[IacResourceProgressStatusLabel]
    delete_failed: _ClassVar[IacResourceProgressStatusLabel]
    replace_failed: _ClassVar[IacResourceProgressStatusLabel]

class IacDiagnosticEventSeverityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    iac_diagnostic_event_severity_type_unspecified: _ClassVar[IacDiagnosticEventSeverityType]
    info: _ClassVar[IacDiagnosticEventSeverityType]
    warning: _ClassVar[IacDiagnosticEventSeverityType]
    error: _ClassVar[IacDiagnosticEventSeverityType]
stack_job_operation_type_unspecified: StackJobOperationType
init: StackJobOperationType
refresh: StackJobOperationType
update_preview: StackJobOperationType
update: StackJobOperationType
destroy_preview: StackJobOperationType
destroy: StackJobOperationType
stack_job_progress_event_type_unspecified: StackJobProgressEventType
stack_job_status_changed_event: StackJobProgressEventType
iac_module_repo_setup_event: StackJobProgressEventType
iac_operation_status_event: StackJobProgressEventType
iac_stack_resources_event: StackJobProgressEventType
iac_stack_outputs_event: StackJobProgressEventType
terraform_engine_event: StackJobProgressEventType
pulumi_engine_event: StackJobProgressEventType
iac_resource_progress_status_label_unspecified: IacResourceProgressStatusLabel
refreshing: IacResourceProgressStatusLabel
unchanged: IacResourceProgressStatusLabel
create: IacResourceProgressStatusLabel
iac_resource_progress_status_label_update: IacResourceProgressStatusLabel
delete: IacResourceProgressStatusLabel
replace: IacResourceProgressStatusLabel
creating: IacResourceProgressStatusLabel
updating: IacResourceProgressStatusLabel
deleting: IacResourceProgressStatusLabel
replacing: IacResourceProgressStatusLabel
refreshed: IacResourceProgressStatusLabel
iac_resource_progress_status_label_created: IacResourceProgressStatusLabel
iac_resource_progress_status_label_updated: IacResourceProgressStatusLabel
iac_resource_progress_status_label_deleted: IacResourceProgressStatusLabel
replaced: IacResourceProgressStatusLabel
refresh_failed: IacResourceProgressStatusLabel
create_failed: IacResourceProgressStatusLabel
update_failed: IacResourceProgressStatusLabel
delete_failed: IacResourceProgressStatusLabel
replace_failed: IacResourceProgressStatusLabel
iac_diagnostic_event_severity_type_unspecified: IacDiagnosticEventSeverityType
info: IacDiagnosticEventSeverityType
warning: IacDiagnosticEventSeverityType
error: IacDiagnosticEventSeverityType
IS_REFRESH_REQUIRED_FIELD_NUMBER: _ClassVar[int]
is_refresh_required: _descriptor.FieldDescriptor
IS_UPDATE_PREVIEW_REQUIRED_FIELD_NUMBER: _ClassVar[int]
is_update_preview_required: _descriptor.FieldDescriptor
IS_DESTROY_PREVIEW_REQUIRED_FIELD_NUMBER: _ClassVar[int]
is_destroy_preview_required: _descriptor.FieldDescriptor
IS_UPDATE_REQUIRED_FIELD_NUMBER: _ClassVar[int]
is_update_required: _descriptor.FieldDescriptor
IS_DESTROY_REQUIRED_FIELD_NUMBER: _ClassVar[int]
is_destroy_required: _descriptor.FieldDescriptor
IS_FINAL_STATUS_FIELD_NUMBER: _ClassVar[int]
is_final_status: _descriptor.FieldDescriptor
