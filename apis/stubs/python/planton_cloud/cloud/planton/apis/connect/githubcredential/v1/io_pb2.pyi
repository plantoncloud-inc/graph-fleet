import datetime

from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.connect.githubcredential.v1 import api_pb2 as _api_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FindGithubRepositoriesInput(_message.Message):
    __slots__ = ("github_credential_id", "search_text")
    GITHUB_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    github_credential_id: str
    search_text: str
    def __init__(self, github_credential_id: _Optional[str] = ..., search_text: _Optional[str] = ...) -> None: ...

class FindGithubRepositoriesResponse(_message.Message):
    __slots__ = ("repos",)
    REPOS_FIELD_NUMBER: _ClassVar[int]
    repos: _containers.RepeatedCompositeFieldContainer[FindGithubRepositoriesResponseItem]
    def __init__(self, repos: _Optional[_Iterable[_Union[FindGithubRepositoriesResponseItem, _Mapping]]] = ...) -> None: ...

class FindGithubRepositoriesResponseItem(_message.Message):
    __slots__ = ("owner_name", "name", "description", "id", "web_url", "clone_url", "default_branch", "last_commit_time")
    OWNER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    WEB_URL_FIELD_NUMBER: _ClassVar[int]
    CLONE_URL_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BRANCH_FIELD_NUMBER: _ClassVar[int]
    LAST_COMMIT_TIME_FIELD_NUMBER: _ClassVar[int]
    owner_name: str
    name: str
    description: str
    id: float
    web_url: str
    clone_url: str
    default_branch: str
    last_commit_time: _timestamp_pb2.Timestamp
    def __init__(self, owner_name: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., id: _Optional[float] = ..., web_url: _Optional[str] = ..., clone_url: _Optional[str] = ..., default_branch: _Optional[str] = ..., last_commit_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GithubAppInstallationId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class GithubRepoWebhookRequest(_message.Message):
    __slots__ = ("github_credential_id", "repo_name")
    GITHUB_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    REPO_NAME_FIELD_NUMBER: _ClassVar[int]
    github_credential_id: str
    repo_name: str
    def __init__(self, github_credential_id: _Optional[str] = ..., repo_name: _Optional[str] = ...) -> None: ...

class GithubWebhookId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class GithubCredentialList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.GithubCredential]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_api_pb2.GithubCredential, _Mapping]]] = ...) -> None: ...
