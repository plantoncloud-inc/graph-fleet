from cloud.planton.apis.connect.terraformbackendcredential.v1 import backend_pb2 as _backend_pb2
from cloud.planton.apis.infrahub.iacmodule.v1 import git_repo_pb2 as _git_repo_pb2
from project.planton.shared.iac.terraform import terraform_pb2 as _terraform_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TerraformStackOperation(_message.Message):
    __slots__ = ("operation", "preview")
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    operation: _terraform_pb2.TerraformOperationType
    preview: bool
    def __init__(self, operation: _Optional[_Union[_terraform_pb2.TerraformOperationType, str]] = ..., preview: bool = ...) -> None: ...

class TerraformStackInfo(_message.Message):
    __slots__ = ("operations", "backend", "backend_object", "git_repo")
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    BACKEND_FIELD_NUMBER: _ClassVar[int]
    BACKEND_OBJECT_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_FIELD_NUMBER: _ClassVar[int]
    operations: _containers.RepeatedCompositeFieldContainer[TerraformStackOperation]
    backend: _backend_pb2.TerraformBackend
    backend_object: str
    git_repo: _git_repo_pb2.IacGitRepo
    def __init__(self, operations: _Optional[_Iterable[_Union[TerraformStackOperation, _Mapping]]] = ..., backend: _Optional[_Union[_backend_pb2.TerraformBackend, _Mapping]] = ..., backend_object: _Optional[str] = ..., git_repo: _Optional[_Union[_git_repo_pb2.IacGitRepo, _Mapping]] = ...) -> None: ...
