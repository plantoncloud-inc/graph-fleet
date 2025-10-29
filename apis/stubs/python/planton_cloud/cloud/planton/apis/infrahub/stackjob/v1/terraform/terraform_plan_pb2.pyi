import datetime

from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTION_TYPE_UNSPECIFIED: _ClassVar[ActionType]
    ACTION_NO_OP: _ClassVar[ActionType]
    ACTION_CREATE: _ClassVar[ActionType]
    ACTION_UPDATE: _ClassVar[ActionType]
    ACTION_DELETE: _ClassVar[ActionType]
    ACTION_REPLACE: _ClassVar[ActionType]
ACTION_TYPE_UNSPECIFIED: ActionType
ACTION_NO_OP: ActionType
ACTION_CREATE: ActionType
ACTION_UPDATE: ActionType
ACTION_DELETE: ActionType
ACTION_REPLACE: ActionType

class Plan(_message.Message):
    __slots__ = ("terraform_version", "variables", "resource_changes", "output_changes", "timestamp", "errored")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Struct
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class OutputChangesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: OutputChange
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[OutputChange, _Mapping]] = ...) -> None: ...
    TERRAFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_CHANGES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CHANGES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ERRORED_FIELD_NUMBER: _ClassVar[int]
    terraform_version: str
    variables: _containers.MessageMap[str, _struct_pb2.Struct]
    resource_changes: _containers.RepeatedCompositeFieldContainer[ResourceChange]
    output_changes: _containers.MessageMap[str, OutputChange]
    timestamp: _timestamp_pb2.Timestamp
    errored: bool
    def __init__(self, terraform_version: _Optional[str] = ..., variables: _Optional[_Mapping[str, _struct_pb2.Struct]] = ..., resource_changes: _Optional[_Iterable[_Union[ResourceChange, _Mapping]]] = ..., output_changes: _Optional[_Mapping[str, OutputChange]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., errored: bool = ...) -> None: ...

class ResourceChange(_message.Message):
    __slots__ = ("address", "mode", "type", "name", "provider_name", "change")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANGE_FIELD_NUMBER: _ClassVar[int]
    address: str
    mode: str
    type: str
    name: str
    provider_name: str
    change: Change
    def __init__(self, address: _Optional[str] = ..., mode: _Optional[str] = ..., type: _Optional[str] = ..., name: _Optional[str] = ..., provider_name: _Optional[str] = ..., change: _Optional[_Union[Change, _Mapping]] = ...) -> None: ...

class Change(_message.Message):
    __slots__ = ("actions", "before", "after", "after_unknown", "before_sensitive", "after_sensitive")
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    AFTER_UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    BEFORE_SENSITIVE_FIELD_NUMBER: _ClassVar[int]
    AFTER_SENSITIVE_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedScalarFieldContainer[ActionType]
    before: _struct_pb2.Struct
    after: _struct_pb2.Struct
    after_unknown: _struct_pb2.Struct
    before_sensitive: bool
    after_sensitive: _struct_pb2.Struct
    def __init__(self, actions: _Optional[_Iterable[_Union[ActionType, str]]] = ..., before: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., after: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., after_unknown: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., before_sensitive: bool = ..., after_sensitive: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class OutputChange(_message.Message):
    __slots__ = ("actions", "before", "after", "after_unknown", "before_sensitive", "after_sensitive")
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    AFTER_UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    BEFORE_SENSITIVE_FIELD_NUMBER: _ClassVar[int]
    AFTER_SENSITIVE_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedScalarFieldContainer[ActionType]
    before: str
    after: str
    after_unknown: bool
    before_sensitive: bool
    after_sensitive: bool
    def __init__(self, actions: _Optional[_Iterable[_Union[ActionType, str]]] = ..., before: _Optional[str] = ..., after: _Optional[str] = ..., after_unknown: bool = ..., before_sensitive: bool = ..., after_sensitive: bool = ...) -> None: ...
