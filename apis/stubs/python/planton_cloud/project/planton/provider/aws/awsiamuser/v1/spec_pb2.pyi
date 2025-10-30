from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsIamUserSpec(_message.Message):
    __slots__ = ("user_name", "managed_policy_arns", "inline_policies", "disable_access_keys")
    class InlinePoliciesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Struct
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    MANAGED_POLICY_ARNS_FIELD_NUMBER: _ClassVar[int]
    INLINE_POLICIES_FIELD_NUMBER: _ClassVar[int]
    DISABLE_ACCESS_KEYS_FIELD_NUMBER: _ClassVar[int]
    user_name: str
    managed_policy_arns: _containers.RepeatedScalarFieldContainer[str]
    inline_policies: _containers.MessageMap[str, _struct_pb2.Struct]
    disable_access_keys: bool
    def __init__(self, user_name: _Optional[str] = ..., managed_policy_arns: _Optional[_Iterable[str]] = ..., inline_policies: _Optional[_Mapping[str, _struct_pb2.Struct]] = ..., disable_access_keys: bool = ...) -> None: ...
