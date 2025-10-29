from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CodegenFindAndReplaceInputInput(_message.Message):
    __slots__ = ("directories", "replacements")
    DIRECTORIES_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENTS_FIELD_NUMBER: _ClassVar[int]
    directories: _containers.RepeatedCompositeFieldContainer[SourceDestinationDirectoryPair]
    replacements: CodegenFindAndReplaceInputInputOrderedReplacements
    def __init__(self, directories: _Optional[_Iterable[_Union[SourceDestinationDirectoryPair, _Mapping]]] = ..., replacements: _Optional[_Union[CodegenFindAndReplaceInputInputOrderedReplacements, _Mapping]] = ...) -> None: ...

class SourceDestinationDirectoryPair(_message.Message):
    __slots__ = ("source", "destination")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    source: str
    destination: str
    def __init__(self, source: _Optional[str] = ..., destination: _Optional[str] = ...) -> None: ...

class CodegenFindAndReplaceInputInputOrderedReplacements(_message.Message):
    __slots__ = ("file_and_dir_name", "file_content")
    FILE_AND_DIR_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    file_and_dir_name: _containers.RepeatedCompositeFieldContainer[FindReplaceStringPair]
    file_content: _containers.RepeatedCompositeFieldContainer[FindReplaceStringPair]
    def __init__(self, file_and_dir_name: _Optional[_Iterable[_Union[FindReplaceStringPair, _Mapping]]] = ..., file_content: _Optional[_Iterable[_Union[FindReplaceStringPair, _Mapping]]] = ...) -> None: ...

class FindReplaceStringPair(_message.Message):
    __slots__ = ("find_string", "replace_string")
    FIND_STRING_FIELD_NUMBER: _ClassVar[int]
    REPLACE_STRING_FIELD_NUMBER: _ClassVar[int]
    find_string: str
    replace_string: str
    def __init__(self, find_string: _Optional[str] = ..., replace_string: _Optional[str] = ...) -> None: ...
