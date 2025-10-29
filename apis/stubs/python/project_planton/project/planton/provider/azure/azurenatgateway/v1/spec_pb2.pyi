from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AzureNatGatewaySpec(_message.Message):
    __slots__ = ("subnet_id", "idle_timeout_minutes", "public_ip_prefix_length", "tags")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SUBNET_ID_FIELD_NUMBER: _ClassVar[int]
    IDLE_TIMEOUT_MINUTES_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IP_PREFIX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    subnet_id: _foreign_key_pb2.StringValueOrRef
    idle_timeout_minutes: int
    public_ip_prefix_length: int
    tags: _containers.ScalarMap[str, str]
    def __init__(self, subnet_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., idle_timeout_minutes: _Optional[int] = ..., public_ip_prefix_length: _Optional[int] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...
