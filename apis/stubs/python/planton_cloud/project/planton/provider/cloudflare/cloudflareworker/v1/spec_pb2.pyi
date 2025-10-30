from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareWorkerSpec(_message.Message):
    __slots__ = ("account_id", "script", "kv_bindings", "dns", "compatibility_date", "usage_model", "env")
    class CloudflareWorkerUsageModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BUNDLED: _ClassVar[CloudflareWorkerSpec.CloudflareWorkerUsageModel]
        UNBOUND: _ClassVar[CloudflareWorkerSpec.CloudflareWorkerUsageModel]
    BUNDLED: CloudflareWorkerSpec.CloudflareWorkerUsageModel
    UNBOUND: CloudflareWorkerSpec.CloudflareWorkerUsageModel
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    KV_BINDINGS_FIELD_NUMBER: _ClassVar[int]
    DNS_FIELD_NUMBER: _ClassVar[int]
    COMPATIBILITY_DATE_FIELD_NUMBER: _ClassVar[int]
    USAGE_MODEL_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    script: CloudflareWorkerScript
    kv_bindings: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.ValueFromRef]
    dns: CloudflareWorkerDns
    compatibility_date: str
    usage_model: CloudflareWorkerSpec.CloudflareWorkerUsageModel
    env: CloudflareWorkerEnv
    def __init__(self, account_id: _Optional[str] = ..., script: _Optional[_Union[CloudflareWorkerScript, _Mapping]] = ..., kv_bindings: _Optional[_Iterable[_Union[_foreign_key_pb2.ValueFromRef, _Mapping]]] = ..., dns: _Optional[_Union[CloudflareWorkerDns, _Mapping]] = ..., compatibility_date: _Optional[str] = ..., usage_model: _Optional[_Union[CloudflareWorkerSpec.CloudflareWorkerUsageModel, str]] = ..., env: _Optional[_Union[CloudflareWorkerEnv, _Mapping]] = ...) -> None: ...

class CloudflareWorkerEnv(_message.Message):
    __slots__ = ("variables", "secrets")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SecretsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.ScalarMap[str, str]
    secrets: _containers.ScalarMap[str, str]
    def __init__(self, variables: _Optional[_Mapping[str, str]] = ..., secrets: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CloudflareWorkerScript(_message.Message):
    __slots__ = ("name", "bundle")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    bundle: CloudflareWorkerScriptBundleR2Object
    def __init__(self, name: _Optional[str] = ..., bundle: _Optional[_Union[CloudflareWorkerScriptBundleR2Object, _Mapping]] = ...) -> None: ...

class CloudflareWorkerScriptBundleR2Object(_message.Message):
    __slots__ = ("bucket", "path")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    path: str
    def __init__(self, bucket: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class CloudflareWorkerDns(_message.Message):
    __slots__ = ("enabled", "zone_id", "hostname", "route_pattern")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    ROUTE_PATTERN_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    zone_id: str
    hostname: str
    route_pattern: str
    def __init__(self, enabled: bool = ..., zone_id: _Optional[str] = ..., hostname: _Optional[str] = ..., route_pattern: _Optional[str] = ...) -> None: ...
