from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.servicehub.secretsgroup.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.servicehub.secretsgroup.v1 import spec_pb2 as _spec_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SecretsGroupId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class TransformSecretKeysRequest(_message.Message):
    __slots__ = ("org", "entries")
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    org: str
    entries: _containers.ScalarMap[str, str]
    def __init__(self, org: _Optional[str] = ..., entries: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TransformSecretKeysResponse(_message.Message):
    __slots__ = ("transformed_entries", "failed_entries")
    class TransformedEntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class FailedEntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TRANSFORMED_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    FAILED_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    transformed_entries: _containers.ScalarMap[str, str]
    failed_entries: _containers.ScalarMap[str, str]
    def __init__(self, transformed_entries: _Optional[_Mapping[str, str]] = ..., failed_entries: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpsertSecretRequest(_message.Message):
    __slots__ = ("group_id", "entry")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    entry: _spec_pb2.SecretsGroupEntry
    def __init__(self, group_id: _Optional[str] = ..., entry: _Optional[_Union[_spec_pb2.SecretsGroupEntry, _Mapping]] = ...) -> None: ...

class DeleteSecretRequest(_message.Message):
    __slots__ = ("group_id", "entry_name")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    entry_name: str
    def __init__(self, group_id: _Optional[str] = ..., entry_name: _Optional[str] = ...) -> None: ...

class GetSecretValueRequest(_message.Message):
    __slots__ = ("org", "group_name", "entry_name")
    ORG_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    org: str
    group_name: str
    entry_name: str
    def __init__(self, org: _Optional[str] = ..., group_name: _Optional[str] = ..., entry_name: _Optional[str] = ...) -> None: ...

class SecretsGroupList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.SecretsGroup]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_api_pb2.SecretsGroup, _Mapping]]] = ...) -> None: ...
