from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.integration.vcs import provider_pb2 as _provider_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GitAuth(_message.Message):
    __slots__ = ("oauth_token", "basic", "ssh_private_key")
    OAUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    BASIC_FIELD_NUMBER: _ClassVar[int]
    SSH_PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    oauth_token: OAuthTokenAuth
    basic: BasicAuth
    ssh_private_key: SshPrivateKeyAuth
    def __init__(self, oauth_token: _Optional[_Union[OAuthTokenAuth, _Mapping]] = ..., basic: _Optional[_Union[BasicAuth, _Mapping]] = ..., ssh_private_key: _Optional[_Union[SshPrivateKeyAuth, _Mapping]] = ...) -> None: ...

class OAuthTokenAuth(_message.Message):
    __slots__ = ("access_token",)
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class BasicAuth(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class SshPrivateKeyAuth(_message.Message):
    __slots__ = ("private_key_pem", "passphrase")
    PRIVATE_KEY_PEM_FIELD_NUMBER: _ClassVar[int]
    PASSPHRASE_FIELD_NUMBER: _ClassVar[int]
    private_key_pem: str
    passphrase: str
    def __init__(self, private_key_pem: _Optional[str] = ..., passphrase: _Optional[str] = ...) -> None: ...

class RepoRef(_message.Message):
    __slots__ = ("provider", "owner_name", "repo_name", "branch", "auth", "host_base_url")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    OWNER_NAME_FIELD_NUMBER: _ClassVar[int]
    REPO_NAME_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    AUTH_FIELD_NUMBER: _ClassVar[int]
    HOST_BASE_URL_FIELD_NUMBER: _ClassVar[int]
    provider: _provider_pb2.GitRepoProvider
    owner_name: str
    repo_name: str
    branch: str
    auth: GitAuth
    host_base_url: str
    def __init__(self, provider: _Optional[_Union[_provider_pb2.GitRepoProvider, str]] = ..., owner_name: _Optional[str] = ..., repo_name: _Optional[str] = ..., branch: _Optional[str] = ..., auth: _Optional[_Union[GitAuth, _Mapping]] = ..., host_base_url: _Optional[str] = ...) -> None: ...

class Branch(_message.Message):
    __slots__ = ("name", "commit_sha", "is_default")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    name: str
    commit_sha: str
    is_default: bool
    def __init__(self, name: _Optional[str] = ..., commit_sha: _Optional[str] = ..., is_default: bool = ...) -> None: ...

class BranchList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[Branch]
    def __init__(self, entries: _Optional[_Iterable[_Union[Branch, _Mapping]]] = ...) -> None: ...

class ListTreeInput(_message.Message):
    __slots__ = ("repo", "path", "recursive", "include_globs", "exclude_globs")
    REPO_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_GLOBS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_GLOBS_FIELD_NUMBER: _ClassVar[int]
    repo: RepoRef
    path: str
    recursive: bool
    include_globs: _containers.RepeatedScalarFieldContainer[str]
    exclude_globs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, repo: _Optional[_Union[RepoRef, _Mapping]] = ..., path: _Optional[str] = ..., recursive: bool = ..., include_globs: _Optional[_Iterable[str]] = ..., exclude_globs: _Optional[_Iterable[str]] = ...) -> None: ...

class TreeEntry(_message.Message):
    __slots__ = ("path", "is_dir", "sha", "size", "last_commit_sha")
    PATH_FIELD_NUMBER: _ClassVar[int]
    IS_DIR_FIELD_NUMBER: _ClassVar[int]
    SHA_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    LAST_COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    path: str
    is_dir: bool
    sha: str
    size: int
    last_commit_sha: str
    def __init__(self, path: _Optional[str] = ..., is_dir: bool = ..., sha: _Optional[str] = ..., size: _Optional[int] = ..., last_commit_sha: _Optional[str] = ...) -> None: ...

class TreeList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[TreeEntry]
    def __init__(self, entries: _Optional[_Iterable[_Union[TreeEntry, _Mapping]]] = ...) -> None: ...

class GetFileInput(_message.Message):
    __slots__ = ("repo", "path")
    REPO_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    repo: RepoRef
    path: str
    def __init__(self, repo: _Optional[_Union[RepoRef, _Mapping]] = ..., path: _Optional[str] = ...) -> None: ...

class FileRef(_message.Message):
    __slots__ = ("path", "sha")
    PATH_FIELD_NUMBER: _ClassVar[int]
    SHA_FIELD_NUMBER: _ClassVar[int]
    path: str
    sha: str
    def __init__(self, path: _Optional[str] = ..., sha: _Optional[str] = ...) -> None: ...

class FileContent(_message.Message):
    __slots__ = ("path", "sha", "content", "encoding")
    PATH_FIELD_NUMBER: _ClassVar[int]
    SHA_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    path: str
    sha: str
    content: bytes
    encoding: str
    def __init__(self, path: _Optional[str] = ..., sha: _Optional[str] = ..., content: _Optional[bytes] = ..., encoding: _Optional[str] = ...) -> None: ...

class FileList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[FileRef]
    def __init__(self, entries: _Optional[_Iterable[_Union[FileRef, _Mapping]]] = ...) -> None: ...

class FindFilesByGlobInput(_message.Message):
    __slots__ = ("repo", "base_path", "include_globs", "exclude_globs")
    REPO_FIELD_NUMBER: _ClassVar[int]
    BASE_PATH_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_GLOBS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_GLOBS_FIELD_NUMBER: _ClassVar[int]
    repo: RepoRef
    base_path: str
    include_globs: _containers.RepeatedScalarFieldContainer[str]
    exclude_globs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, repo: _Optional[_Union[RepoRef, _Mapping]] = ..., base_path: _Optional[str] = ..., include_globs: _Optional[_Iterable[str]] = ..., exclude_globs: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateBranchInput(_message.Message):
    __slots__ = ("repo", "new_branch_name", "from_commit_sha")
    REPO_FIELD_NUMBER: _ClassVar[int]
    NEW_BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    FROM_COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    repo: RepoRef
    new_branch_name: str
    from_commit_sha: str
    def __init__(self, repo: _Optional[_Union[RepoRef, _Mapping]] = ..., new_branch_name: _Optional[str] = ..., from_commit_sha: _Optional[str] = ...) -> None: ...

class UpdateFileInput(_message.Message):
    __slots__ = ("repo", "path", "content", "expected_base_sha", "commit_message")
    REPO_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_BASE_SHA_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    repo: RepoRef
    path: str
    content: bytes
    expected_base_sha: str
    commit_message: str
    def __init__(self, repo: _Optional[_Union[RepoRef, _Mapping]] = ..., path: _Optional[str] = ..., content: _Optional[bytes] = ..., expected_base_sha: _Optional[str] = ..., commit_message: _Optional[str] = ...) -> None: ...

class UpdateFileResponse(_message.Message):
    __slots__ = ("new_sha", "commit_sha", "branch")
    NEW_SHA_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    new_sha: str
    commit_sha: str
    branch: str
    def __init__(self, new_sha: _Optional[str] = ..., commit_sha: _Optional[str] = ..., branch: _Optional[str] = ...) -> None: ...

class OpenPullRequestInput(_message.Message):
    __slots__ = ("repo", "head_branch", "base_branch", "title", "body")
    REPO_FIELD_NUMBER: _ClassVar[int]
    HEAD_BRANCH_FIELD_NUMBER: _ClassVar[int]
    BASE_BRANCH_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    repo: RepoRef
    head_branch: str
    base_branch: str
    title: str
    body: str
    def __init__(self, repo: _Optional[_Union[RepoRef, _Mapping]] = ..., head_branch: _Optional[str] = ..., base_branch: _Optional[str] = ..., title: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...

class OpenPullRequestResponse(_message.Message):
    __slots__ = ("pr_url", "pr_number")
    PR_URL_FIELD_NUMBER: _ClassVar[int]
    PR_NUMBER_FIELD_NUMBER: _ClassVar[int]
    pr_url: str
    pr_number: int
    def __init__(self, pr_url: _Optional[str] = ..., pr_number: _Optional[int] = ...) -> None: ...
