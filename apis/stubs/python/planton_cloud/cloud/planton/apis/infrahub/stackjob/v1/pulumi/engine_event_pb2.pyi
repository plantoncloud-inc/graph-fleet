from cloud.planton.apis.infrahub.stackjob.v1.pulumi import enum_pb2 as _enum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiffKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIFF_KIND_UNSPECIFIED: _ClassVar[DiffKind]
    DIFF_ADD: _ClassVar[DiffKind]
    DIFF_ADD_REPLACE: _ClassVar[DiffKind]
    DIFF_DELETE: _ClassVar[DiffKind]
    DIFF_DELETE_REPLACE: _ClassVar[DiffKind]
    DIFF_UPDATE: _ClassVar[DiffKind]
    DIFF_UPDATE_REPLACE: _ClassVar[DiffKind]
DIFF_KIND_UNSPECIFIED: DiffKind
DIFF_ADD: DiffKind
DIFF_ADD_REPLACE: DiffKind
DIFF_DELETE: DiffKind
DIFF_DELETE_REPLACE: DiffKind
DIFF_UPDATE: DiffKind
DIFF_UPDATE_REPLACE: DiffKind

class CancelEvent(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StdoutEngineEvent(_message.Message):
    __slots__ = ("message", "color")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    message: str
    color: str
    def __init__(self, message: _Optional[str] = ..., color: _Optional[str] = ...) -> None: ...

class DiagnosticEvent(_message.Message):
    __slots__ = ("urn", "prefix", "message", "color", "severity", "stream_id", "ephemeral")
    URN_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_FIELD_NUMBER: _ClassVar[int]
    urn: str
    prefix: str
    message: str
    color: str
    severity: str
    stream_id: int
    ephemeral: bool
    def __init__(self, urn: _Optional[str] = ..., prefix: _Optional[str] = ..., message: _Optional[str] = ..., color: _Optional[str] = ..., severity: _Optional[str] = ..., stream_id: _Optional[int] = ..., ephemeral: bool = ...) -> None: ...

class PolicyEvent(_message.Message):
    __slots__ = ("resource_urn", "message", "color", "policy_name", "policy_pack_name", "policy_pack_version", "policy_pack_version_tag", "enforcement_level")
    RESOURCE_URN_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    POLICY_NAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_PACK_NAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_PACK_VERSION_FIELD_NUMBER: _ClassVar[int]
    POLICY_PACK_VERSION_TAG_FIELD_NUMBER: _ClassVar[int]
    ENFORCEMENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    resource_urn: str
    message: str
    color: str
    policy_name: str
    policy_pack_name: str
    policy_pack_version: str
    policy_pack_version_tag: str
    enforcement_level: str
    def __init__(self, resource_urn: _Optional[str] = ..., message: _Optional[str] = ..., color: _Optional[str] = ..., policy_name: _Optional[str] = ..., policy_pack_name: _Optional[str] = ..., policy_pack_version: _Optional[str] = ..., policy_pack_version_tag: _Optional[str] = ..., enforcement_level: _Optional[str] = ...) -> None: ...

class PolicyRemediationEvent(_message.Message):
    __slots__ = ("resource_urn", "color", "policy_name", "policy_pack_name", "policy_pack_version", "policy_pack_version_tag", "before", "after")
    class BeforeEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class AfterEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    RESOURCE_URN_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    POLICY_NAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_PACK_NAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_PACK_VERSION_FIELD_NUMBER: _ClassVar[int]
    POLICY_PACK_VERSION_TAG_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    resource_urn: str
    color: str
    policy_name: str
    policy_pack_name: str
    policy_pack_version: str
    policy_pack_version_tag: str
    before: _containers.ScalarMap[str, str]
    after: _containers.ScalarMap[str, str]
    def __init__(self, resource_urn: _Optional[str] = ..., color: _Optional[str] = ..., policy_name: _Optional[str] = ..., policy_pack_name: _Optional[str] = ..., policy_pack_version: _Optional[str] = ..., policy_pack_version_tag: _Optional[str] = ..., before: _Optional[_Mapping[str, str]] = ..., after: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PreludeEvent(_message.Message):
    __slots__ = ("config",)
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _containers.ScalarMap[str, str]
    def __init__(self, config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SummaryEvent(_message.Message):
    __slots__ = ("maybe_corrupt", "duration_seconds", "resource_changes", "policy_packs")
    class ResourceChangesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class PolicyPacksEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    MAYBE_CORRUPT_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_CHANGES_FIELD_NUMBER: _ClassVar[int]
    POLICY_PACKS_FIELD_NUMBER: _ClassVar[int]
    maybe_corrupt: bool
    duration_seconds: int
    resource_changes: _containers.ScalarMap[str, int]
    policy_packs: _containers.ScalarMap[str, str]
    def __init__(self, maybe_corrupt: bool = ..., duration_seconds: _Optional[int] = ..., resource_changes: _Optional[_Mapping[str, int]] = ..., policy_packs: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PropertyDiff(_message.Message):
    __slots__ = ("diff_kind", "input_diff")
    DIFF_KIND_FIELD_NUMBER: _ClassVar[int]
    INPUT_DIFF_FIELD_NUMBER: _ClassVar[int]
    diff_kind: DiffKind
    input_diff: bool
    def __init__(self, diff_kind: _Optional[_Union[DiffKind, str]] = ..., input_diff: bool = ...) -> None: ...

class StepEventMetadata(_message.Message):
    __slots__ = ("op", "urn", "type", "old", "new", "keys", "diffs", "detailed_diff", "logical", "provider")
    class DetailedDiffEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PropertyDiff
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[PropertyDiff, _Mapping]] = ...) -> None: ...
    OP_FIELD_NUMBER: _ClassVar[int]
    URN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OLD_FIELD_NUMBER: _ClassVar[int]
    NEW_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    DIFFS_FIELD_NUMBER: _ClassVar[int]
    DETAILED_DIFF_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    op: _enum_pb2.PulumiEngineOperationType
    urn: str
    type: str
    old: StepEventStateMetadata
    new: StepEventStateMetadata
    keys: _containers.RepeatedScalarFieldContainer[str]
    diffs: _containers.RepeatedScalarFieldContainer[str]
    detailed_diff: _containers.MessageMap[str, PropertyDiff]
    logical: bool
    provider: str
    def __init__(self, op: _Optional[_Union[_enum_pb2.PulumiEngineOperationType, str]] = ..., urn: _Optional[str] = ..., type: _Optional[str] = ..., old: _Optional[_Union[StepEventStateMetadata, _Mapping]] = ..., new: _Optional[_Union[StepEventStateMetadata, _Mapping]] = ..., keys: _Optional[_Iterable[str]] = ..., diffs: _Optional[_Iterable[str]] = ..., detailed_diff: _Optional[_Mapping[str, PropertyDiff]] = ..., logical: bool = ..., provider: _Optional[str] = ...) -> None: ...

class StepEventStateMetadata(_message.Message):
    __slots__ = ("type", "urn", "custom", "delete", "id", "parent", "protect", "retain_on_delete", "inputs", "outputs", "provider", "init_errors")
    class InputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class OutputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    URN_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PROTECT_FIELD_NUMBER: _ClassVar[int]
    RETAIN_ON_DELETE_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    INIT_ERRORS_FIELD_NUMBER: _ClassVar[int]
    type: str
    urn: str
    custom: bool
    delete: bool
    id: str
    parent: str
    protect: bool
    retain_on_delete: bool
    inputs: _containers.ScalarMap[str, str]
    outputs: _containers.ScalarMap[str, str]
    provider: str
    init_errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, type: _Optional[str] = ..., urn: _Optional[str] = ..., custom: bool = ..., delete: bool = ..., id: _Optional[str] = ..., parent: _Optional[str] = ..., protect: bool = ..., retain_on_delete: bool = ..., inputs: _Optional[_Mapping[str, str]] = ..., outputs: _Optional[_Mapping[str, str]] = ..., provider: _Optional[str] = ..., init_errors: _Optional[_Iterable[str]] = ...) -> None: ...

class ResourcePreEvent(_message.Message):
    __slots__ = ("metadata", "planning")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PLANNING_FIELD_NUMBER: _ClassVar[int]
    metadata: StepEventMetadata
    planning: bool
    def __init__(self, metadata: _Optional[_Union[StepEventMetadata, _Mapping]] = ..., planning: bool = ...) -> None: ...

class ResOutputsEvent(_message.Message):
    __slots__ = ("metadata", "planning")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PLANNING_FIELD_NUMBER: _ClassVar[int]
    metadata: StepEventMetadata
    planning: bool
    def __init__(self, metadata: _Optional[_Union[StepEventMetadata, _Mapping]] = ..., planning: bool = ...) -> None: ...

class ResOpFailedEvent(_message.Message):
    __slots__ = ("metadata", "status", "steps")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    metadata: StepEventMetadata
    status: int
    steps: int
    def __init__(self, metadata: _Optional[_Union[StepEventMetadata, _Mapping]] = ..., status: _Optional[int] = ..., steps: _Optional[int] = ...) -> None: ...
