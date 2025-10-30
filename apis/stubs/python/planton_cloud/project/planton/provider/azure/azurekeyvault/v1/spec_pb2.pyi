from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AzureKeyVaultSpec(_message.Message):
    __slots__ = ("secret_names",)
    SECRET_NAMES_FIELD_NUMBER: _ClassVar[int]
    secret_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, secret_names: _Optional[_Iterable[str]] = ...) -> None: ...
