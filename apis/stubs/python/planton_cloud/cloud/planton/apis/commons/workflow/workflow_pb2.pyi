from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class WorkflowExecutionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    workflow_execution_status_unspecified: _ClassVar[WorkflowExecutionStatus]
    queued: _ClassVar[WorkflowExecutionStatus]
    running: _ClassVar[WorkflowExecutionStatus]
    completed: _ClassVar[WorkflowExecutionStatus]
    awaiting_approval: _ClassVar[WorkflowExecutionStatus]

class WorkflowExecutionResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    workflow_execution_result_unspecified: _ClassVar[WorkflowExecutionResult]
    tbd: _ClassVar[WorkflowExecutionResult]
    succeeded: _ClassVar[WorkflowExecutionResult]
    failed: _ClassVar[WorkflowExecutionResult]
    cancelled: _ClassVar[WorkflowExecutionResult]
    skipped: _ClassVar[WorkflowExecutionResult]

class WorkflowStepManualGateDecision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    workflow_step_manual_gate_decision_unspecified: _ClassVar[WorkflowStepManualGateDecision]
    yes: _ClassVar[WorkflowStepManualGateDecision]
    no: _ClassVar[WorkflowStepManualGateDecision]
workflow_execution_status_unspecified: WorkflowExecutionStatus
queued: WorkflowExecutionStatus
running: WorkflowExecutionStatus
completed: WorkflowExecutionStatus
awaiting_approval: WorkflowExecutionStatus
workflow_execution_result_unspecified: WorkflowExecutionResult
tbd: WorkflowExecutionResult
succeeded: WorkflowExecutionResult
failed: WorkflowExecutionResult
cancelled: WorkflowExecutionResult
skipped: WorkflowExecutionResult
workflow_step_manual_gate_decision_unspecified: WorkflowStepManualGateDecision
yes: WorkflowStepManualGateDecision
no: WorkflowStepManualGateDecision
