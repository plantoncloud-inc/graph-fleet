from cloud.planton.apis.connect.pulumibackendcredential.v1 import backend_pb2 as _backend_pb2
from cloud.planton.apis.infrahub.iacmodule.v1 import git_repo_pb2 as _git_repo_pb2
from project.planton.shared.iac.pulumi import pulumi_pb2 as _pulumi_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PulumiProjectRuntime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    pulumi_project_runtime_unspecified: _ClassVar[PulumiProjectRuntime]
    nodejs: _ClassVar[PulumiProjectRuntime]
    python: _ClassVar[PulumiProjectRuntime]
    go: _ClassVar[PulumiProjectRuntime]
    dotnet: _ClassVar[PulumiProjectRuntime]
    java: _ClassVar[PulumiProjectRuntime]
    yaml: _ClassVar[PulumiProjectRuntime]
pulumi_project_runtime_unspecified: PulumiProjectRuntime
nodejs: PulumiProjectRuntime
python: PulumiProjectRuntime
go: PulumiProjectRuntime
dotnet: PulumiProjectRuntime
java: PulumiProjectRuntime
yaml: PulumiProjectRuntime

class PulumiStackOperation(_message.Message):
    __slots__ = ("operation", "preview")
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    operation: _pulumi_pb2.PulumiOperationType
    preview: bool
    def __init__(self, operation: _Optional[_Union[_pulumi_pb2.PulumiOperationType, str]] = ..., preview: bool = ...) -> None: ...

class PulumiProject(_message.Message):
    __slots__ = ("name", "runtime")
    NAME_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    runtime: PulumiProjectRuntime
    def __init__(self, name: _Optional[str] = ..., runtime: _Optional[_Union[PulumiProjectRuntime, str]] = ...) -> None: ...

class PulumiStackInfo(_message.Message):
    __slots__ = ("operations", "backend", "project", "stack_name", "stack_fqdn", "git_repo")
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    BACKEND_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    STACK_NAME_FIELD_NUMBER: _ClassVar[int]
    STACK_FQDN_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_FIELD_NUMBER: _ClassVar[int]
    operations: _containers.RepeatedCompositeFieldContainer[PulumiStackOperation]
    backend: _backend_pb2.PulumiBackend
    project: PulumiProject
    stack_name: str
    stack_fqdn: str
    git_repo: _git_repo_pb2.IacGitRepo
    def __init__(self, operations: _Optional[_Iterable[_Union[PulumiStackOperation, _Mapping]]] = ..., backend: _Optional[_Union[_backend_pb2.PulumiBackend, _Mapping]] = ..., project: _Optional[_Union[PulumiProject, _Mapping]] = ..., stack_name: _Optional[str] = ..., stack_fqdn: _Optional[str] = ..., git_repo: _Optional[_Union[_git_repo_pb2.IacGitRepo, _Mapping]] = ...) -> None: ...
