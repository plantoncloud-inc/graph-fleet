from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TeamId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class RevokeMemberAccessOnTeamsInput(_message.Message):
    __slots__ = ("team_ids", "member_id")
    TEAM_IDS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    team_ids: _containers.RepeatedScalarFieldContainer[str]
    member_id: str
    def __init__(self, team_ids: _Optional[_Iterable[str]] = ..., member_id: _Optional[str] = ...) -> None: ...
