from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EdismaxFieldConfig(_message.Message):
    __slots__ = ("field_name", "partial_boost", "phrase_boost", "bf_term_freq_boost")
    FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_BOOST_FIELD_NUMBER: _ClassVar[int]
    PHRASE_BOOST_FIELD_NUMBER: _ClassVar[int]
    BF_TERM_FREQ_BOOST_FIELD_NUMBER: _ClassVar[int]
    field_name: str
    partial_boost: int
    phrase_boost: int
    bf_term_freq_boost: int
    def __init__(self, field_name: _Optional[str] = ..., partial_boost: _Optional[int] = ..., phrase_boost: _Optional[int] = ..., bf_term_freq_boost: _Optional[int] = ...) -> None: ...
