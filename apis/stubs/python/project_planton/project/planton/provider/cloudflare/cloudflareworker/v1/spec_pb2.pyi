from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareWorkerUsageModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUNDLED: _ClassVar[CloudflareWorkerUsageModel]
    UNBOUND: _ClassVar[CloudflareWorkerUsageModel]
BUNDLED: CloudflareWorkerUsageModel
UNBOUND: CloudflareWorkerUsageModel

class CloudflareWorkerSpec(_message.Message):
    __slots__ = ("script_name", "script_source", "account_id", "kv_bindings", "route_pattern", "compatibility_date", "usage_model", "env_vars")
    class EnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SCRIPT_NAME_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    KV_BINDINGS_FIELD_NUMBER: _ClassVar[int]
    ROUTE_PATTERN_FIELD_NUMBER: _ClassVar[int]
    COMPATIBILITY_DATE_FIELD_NUMBER: _ClassVar[int]
    USAGE_MODEL_FIELD_NUMBER: _ClassVar[int]
    ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    script_name: str
    script_source: _foreign_key_pb2.StringValueOrRef
    account_id: str
    kv_bindings: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.ValueFromRef]
    route_pattern: str
    compatibility_date: str
    usage_model: CloudflareWorkerUsageModel
    env_vars: _containers.ScalarMap[str, str]
    def __init__(self, script_name: _Optional[str] = ..., script_source: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., account_id: _Optional[str] = ..., kv_bindings: _Optional[_Iterable[_Union[_foreign_key_pb2.ValueFromRef, _Mapping]]] = ..., route_pattern: _Optional[str] = ..., compatibility_date: _Optional[str] = ..., usage_model: _Optional[_Union[CloudflareWorkerUsageModel, str]] = ..., env_vars: _Optional[_Mapping[str, str]] = ...) -> None: ...
