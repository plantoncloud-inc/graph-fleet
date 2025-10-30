from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsIamRoleSpec(_message.Message):
    __slots__ = ("description", "path", "trust_policy", "managed_policy_arns", "inline_policies")
    class InlinePoliciesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Struct
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TRUST_POLICY_FIELD_NUMBER: _ClassVar[int]
    MANAGED_POLICY_ARNS_FIELD_NUMBER: _ClassVar[int]
    INLINE_POLICIES_FIELD_NUMBER: _ClassVar[int]
    description: str
    path: str
    trust_policy: _struct_pb2.Struct
    managed_policy_arns: _containers.RepeatedScalarFieldContainer[str]
    inline_policies: _containers.MessageMap[str, _struct_pb2.Struct]
    def __init__(self, description: _Optional[str] = ..., path: _Optional[str] = ..., trust_policy: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., managed_policy_arns: _Optional[_Iterable[str]] = ..., inline_policies: _Optional[_Mapping[str, _struct_pb2.Struct]] = ...) -> None: ...
