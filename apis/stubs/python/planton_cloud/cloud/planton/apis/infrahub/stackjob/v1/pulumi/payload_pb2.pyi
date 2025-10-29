from cloud.planton.apis.infrahub.stackjob.v1.pulumi import engine_event_pb2 as _engine_event_pb2
from cloud.planton.apis.infrahub.stackjob.v1.pulumi import enum_pb2 as _enum_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PulumiEngineEventPayload(_message.Message):
    __slots__ = ("event_type", "sequence", "timestamp", "diff", "cancel_event", "stdout_event", "diagnostic_event", "prelude_event", "summary_event", "resource_pre_event", "res_outputs_event", "res_op_failed_event", "policy_event", "policy_remediation_event")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DIFF_FIELD_NUMBER: _ClassVar[int]
    CANCEL_EVENT_FIELD_NUMBER: _ClassVar[int]
    STDOUT_EVENT_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTIC_EVENT_FIELD_NUMBER: _ClassVar[int]
    PRELUDE_EVENT_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_EVENT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PRE_EVENT_FIELD_NUMBER: _ClassVar[int]
    RES_OUTPUTS_EVENT_FIELD_NUMBER: _ClassVar[int]
    RES_OP_FAILED_EVENT_FIELD_NUMBER: _ClassVar[int]
    POLICY_EVENT_FIELD_NUMBER: _ClassVar[int]
    POLICY_REMEDIATION_EVENT_FIELD_NUMBER: _ClassVar[int]
    event_type: _enum_pb2.PulumiEngineEventType
    sequence: int
    timestamp: int
    diff: str
    cancel_event: _engine_event_pb2.CancelEvent
    stdout_event: _engine_event_pb2.StdoutEngineEvent
    diagnostic_event: _engine_event_pb2.DiagnosticEvent
    prelude_event: _engine_event_pb2.PreludeEvent
    summary_event: _engine_event_pb2.SummaryEvent
    resource_pre_event: _engine_event_pb2.ResourcePreEvent
    res_outputs_event: _engine_event_pb2.ResOutputsEvent
    res_op_failed_event: _engine_event_pb2.ResOpFailedEvent
    policy_event: _engine_event_pb2.PolicyEvent
    policy_remediation_event: _engine_event_pb2.PolicyRemediationEvent
    def __init__(self, event_type: _Optional[_Union[_enum_pb2.PulumiEngineEventType, str]] = ..., sequence: _Optional[int] = ..., timestamp: _Optional[int] = ..., diff: _Optional[str] = ..., cancel_event: _Optional[_Union[_engine_event_pb2.CancelEvent, _Mapping]] = ..., stdout_event: _Optional[_Union[_engine_event_pb2.StdoutEngineEvent, _Mapping]] = ..., diagnostic_event: _Optional[_Union[_engine_event_pb2.DiagnosticEvent, _Mapping]] = ..., prelude_event: _Optional[_Union[_engine_event_pb2.PreludeEvent, _Mapping]] = ..., summary_event: _Optional[_Union[_engine_event_pb2.SummaryEvent, _Mapping]] = ..., resource_pre_event: _Optional[_Union[_engine_event_pb2.ResourcePreEvent, _Mapping]] = ..., res_outputs_event: _Optional[_Union[_engine_event_pb2.ResOutputsEvent, _Mapping]] = ..., res_op_failed_event: _Optional[_Union[_engine_event_pb2.ResOpFailedEvent, _Mapping]] = ..., policy_event: _Optional[_Union[_engine_event_pb2.PolicyEvent, _Mapping]] = ..., policy_remediation_event: _Optional[_Union[_engine_event_pb2.PolicyRemediationEvent, _Mapping]] = ...) -> None: ...
