from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class GitRepoProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    git_repo_provider_unspecified: _ClassVar[GitRepoProvider]
    github: _ClassVar[GitRepoProvider]
    gitlab: _ClassVar[GitRepoProvider]
git_repo_provider_unspecified: GitRepoProvider
github: GitRepoProvider
gitlab: GitRepoProvider
