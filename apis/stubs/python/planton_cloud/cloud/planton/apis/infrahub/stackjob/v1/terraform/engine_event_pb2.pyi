from cloud.planton.apis.infrahub.stackjob.v1.terraform import enum_pb2 as _enum_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TerraformEngineEventJsonLog(_message.Message):
    __slots__ = ("message", "level", "module", "timestamp", "tofu", "ui", "type", "diagnostic", "outputs", "hook", "change", "change_summary")
    class OutputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TerraformEngineJsonLogOutput
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[TerraformEngineJsonLogOutput, _Mapping]] = ...) -> None: ...
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TOFU_FIELD_NUMBER: _ClassVar[int]
    UI_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTIC_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    HOOK_FIELD_NUMBER: _ClassVar[int]
    CHANGE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    message: str
    level: str
    module: str
    timestamp: str
    tofu: str
    ui: str
    type: _enum_pb2.TerraformEngineEventType
    diagnostic: TerraformEngineEventJsonLogDiagnostic
    outputs: _containers.MessageMap[str, TerraformEngineJsonLogOutput]
    hook: TerraformEngineEventJsonLogHook
    change: TerraformEngineEventJsonResourceChange
    change_summary: TerraformEngineEventJsonChangeSummary
    def __init__(self, message: _Optional[str] = ..., level: _Optional[str] = ..., module: _Optional[str] = ..., timestamp: _Optional[str] = ..., tofu: _Optional[str] = ..., ui: _Optional[str] = ..., type: _Optional[_Union[_enum_pb2.TerraformEngineEventType, str]] = ..., diagnostic: _Optional[_Union[TerraformEngineEventJsonLogDiagnostic, _Mapping]] = ..., outputs: _Optional[_Mapping[str, TerraformEngineJsonLogOutput]] = ..., hook: _Optional[_Union[TerraformEngineEventJsonLogHook, _Mapping]] = ..., change: _Optional[_Union[TerraformEngineEventJsonResourceChange, _Mapping]] = ..., change_summary: _Optional[_Union[TerraformEngineEventJsonChangeSummary, _Mapping]] = ...) -> None: ...

class TerraformEngineEventJsonResourceChange(_message.Message):
    __slots__ = ("resource", "previous_resource", "action", "reason")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    resource: TerraformEngineEventJsonLogResource
    previous_resource: TerraformEngineEventJsonLogResource
    action: _enum_pb2.TerraformEngineOperationType
    reason: str
    def __init__(self, resource: _Optional[_Union[TerraformEngineEventJsonLogResource, _Mapping]] = ..., previous_resource: _Optional[_Union[TerraformEngineEventJsonLogResource, _Mapping]] = ..., action: _Optional[_Union[_enum_pb2.TerraformEngineOperationType, str]] = ..., reason: _Optional[str] = ...) -> None: ...

class TerraformEngineEventJsonChangeSummary(_message.Message):
    __slots__ = ("add", "change", "remove", "operation")
    ADD_FIELD_NUMBER: _ClassVar[int]
    CHANGE_FIELD_NUMBER: _ClassVar[int]
    REMOVE_FIELD_NUMBER: _ClassVar[int]
    IMPORT_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    add: int
    change: int
    remove: int
    operation: str
    def __init__(self, add: _Optional[int] = ..., change: _Optional[int] = ..., remove: _Optional[int] = ..., operation: _Optional[str] = ..., **kwargs) -> None: ...

class TerraformEngineEventJsonLogDiagnostic(_message.Message):
    __slots__ = ("severity", "summary", "detail", "address", "range", "snippet")
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    SNIPPET_FIELD_NUMBER: _ClassVar[int]
    severity: str
    summary: str
    detail: str
    address: str
    range: TerraformEngineEventJsonLogDiagnosticRange
    snippet: TerraformEngineEventJsonLogDiagnosticSnippet
    def __init__(self, severity: _Optional[str] = ..., summary: _Optional[str] = ..., detail: _Optional[str] = ..., address: _Optional[str] = ..., range: _Optional[_Union[TerraformEngineEventJsonLogDiagnosticRange, _Mapping]] = ..., snippet: _Optional[_Union[TerraformEngineEventJsonLogDiagnosticSnippet, _Mapping]] = ...) -> None: ...

class TerraformEngineEventJsonLogDiagnosticRange(_message.Message):
    __slots__ = ("filename", "start", "end")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    filename: str
    start: TerraformEngineEventJsonLogDiagnosticRangePos
    end: TerraformEngineEventJsonLogDiagnosticRangePos
    def __init__(self, filename: _Optional[str] = ..., start: _Optional[_Union[TerraformEngineEventJsonLogDiagnosticRangePos, _Mapping]] = ..., end: _Optional[_Union[TerraformEngineEventJsonLogDiagnosticRangePos, _Mapping]] = ...) -> None: ...

class TerraformEngineEventJsonLogDiagnosticRangePos(_message.Message):
    __slots__ = ("line", "column", "byte")
    LINE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    BYTE_FIELD_NUMBER: _ClassVar[int]
    line: int
    column: int
    byte: int
    def __init__(self, line: _Optional[int] = ..., column: _Optional[int] = ..., byte: _Optional[int] = ...) -> None: ...

class TerraformEngineEventJsonLogDiagnosticSnippet(_message.Message):
    __slots__ = ("context", "code", "start_line", "highlight_start_offset", "highlight_end_offset", "values", "function_call")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHT_START_OFFSET_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHT_END_OFFSET_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_FIELD_NUMBER: _ClassVar[int]
    context: str
    code: str
    start_line: int
    highlight_start_offset: int
    highlight_end_offset: int
    values: _containers.RepeatedCompositeFieldContainer[TerraformEngineEventJsonLogDiagnosticExpressionValue]
    function_call: TerraformEngineEventJsonLogDiagnosticFunctionCall
    def __init__(self, context: _Optional[str] = ..., code: _Optional[str] = ..., start_line: _Optional[int] = ..., highlight_start_offset: _Optional[int] = ..., highlight_end_offset: _Optional[int] = ..., values: _Optional[_Iterable[_Union[TerraformEngineEventJsonLogDiagnosticExpressionValue, _Mapping]]] = ..., function_call: _Optional[_Union[TerraformEngineEventJsonLogDiagnosticFunctionCall, _Mapping]] = ...) -> None: ...

class TerraformEngineEventJsonLogDiagnosticExpressionValue(_message.Message):
    __slots__ = ("traversal", "statement")
    TRAVERSAL_FIELD_NUMBER: _ClassVar[int]
    STATEMENT_FIELD_NUMBER: _ClassVar[int]
    traversal: str
    statement: str
    def __init__(self, traversal: _Optional[str] = ..., statement: _Optional[str] = ...) -> None: ...

class TerraformEngineEventJsonLogDiagnosticFunctionCall(_message.Message):
    __slots__ = ("called_as", "signature")
    CALLED_AS_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    called_as: str
    signature: TerraformEngineEventJsonLogDiagnosticFunction
    def __init__(self, called_as: _Optional[str] = ..., signature: _Optional[_Union[TerraformEngineEventJsonLogDiagnosticFunction, _Mapping]] = ...) -> None: ...

class TerraformEngineEventJsonLogDiagnosticFunction(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TerraformEngineEventJsonLogHook(_message.Message):
    __slots__ = ("resource", "id_key", "id_value", "provisioner", "output", "action", "elapsed_seconds")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ID_KEY_FIELD_NUMBER: _ClassVar[int]
    ID_VALUE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONER_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    resource: TerraformEngineEventJsonLogResource
    id_key: str
    id_value: str
    provisioner: str
    output: str
    action: _enum_pb2.TerraformEngineOperationType
    elapsed_seconds: int
    def __init__(self, resource: _Optional[_Union[TerraformEngineEventJsonLogResource, _Mapping]] = ..., id_key: _Optional[str] = ..., id_value: _Optional[str] = ..., provisioner: _Optional[str] = ..., output: _Optional[str] = ..., action: _Optional[_Union[_enum_pb2.TerraformEngineOperationType, str]] = ..., elapsed_seconds: _Optional[int] = ...) -> None: ...

class TerraformEngineEventJsonLogResource(_message.Message):
    __slots__ = ("addr", "module", "resource", "implied_provider", "resource_type", "resource_name", "resource_key")
    ADDR_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    IMPLIED_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_KEY_FIELD_NUMBER: _ClassVar[int]
    addr: str
    module: str
    resource: str
    implied_provider: str
    resource_type: str
    resource_name: str
    resource_key: str
    def __init__(self, addr: _Optional[str] = ..., module: _Optional[str] = ..., resource: _Optional[str] = ..., implied_provider: _Optional[str] = ..., resource_type: _Optional[str] = ..., resource_name: _Optional[str] = ..., resource_key: _Optional[str] = ...) -> None: ...

class TerraformEngineJsonLogOutput(_message.Message):
    __slots__ = ("sensitive", "type", "value", "action")
    SENSITIVE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    sensitive: bool
    type: _struct_pb2.Value
    value: _struct_pb2.Value
    action: _enum_pb2.TerraformEngineOperationType
    def __init__(self, sensitive: bool = ..., type: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., action: _Optional[_Union[_enum_pb2.TerraformEngineOperationType, str]] = ...) -> None: ...
