from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestMessage(_message.Message):
    __slots__ = ("root_level_string", "level_one_message")
    ROOT_LEVEL_STRING_FIELD_NUMBER: _ClassVar[int]
    LEVEL_ONE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    root_level_string: str
    level_one_message: LevelOne
    def __init__(self, root_level_string: _Optional[str] = ..., level_one_message: _Optional[_Union[LevelOne, _Mapping]] = ...) -> None: ...

class LevelOne(_message.Message):
    __slots__ = ("level_one_string", "level_two_message")
    LEVEL_ONE_STRING_FIELD_NUMBER: _ClassVar[int]
    LEVEL_TWO_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    level_one_string: str
    level_two_message: LevelTwo
    def __init__(self, level_one_string: _Optional[str] = ..., level_two_message: _Optional[_Union[LevelTwo, _Mapping]] = ...) -> None: ...

class LevelTwo(_message.Message):
    __slots__ = ("level_two_string", "level_three_message")
    LEVEL_TWO_STRING_FIELD_NUMBER: _ClassVar[int]
    LEVEL_THREE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    level_two_string: str
    level_three_message: LevelThree
    def __init__(self, level_two_string: _Optional[str] = ..., level_three_message: _Optional[_Union[LevelThree, _Mapping]] = ...) -> None: ...

class LevelThree(_message.Message):
    __slots__ = ("level_three_string", "not_a_string")
    LEVEL_THREE_STRING_FIELD_NUMBER: _ClassVar[int]
    NOT_A_STRING_FIELD_NUMBER: _ClassVar[int]
    level_three_string: str
    not_a_string: int
    def __init__(self, level_three_string: _Optional[str] = ..., not_a_string: _Optional[int] = ...) -> None: ...
