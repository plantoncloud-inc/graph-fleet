from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AgentFramework(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    agent_framework_unspecified: _ClassVar[AgentFramework]
    langgraph: _ClassVar[AgentFramework]

class AgentRuntime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    agent_runtime_unspecified: _ClassVar[AgentRuntime]
    python: _ClassVar[AgentRuntime]
agent_framework_unspecified: AgentFramework
langgraph: AgentFramework
agent_runtime_unspecified: AgentRuntime
python: AgentRuntime

class AgentSpec(_message.Message):
    __slots__ = ("description", "framework", "runtime", "icon_url", "git_repo", "is_ready", "langgraph")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    GIT_REPO_FIELD_NUMBER: _ClassVar[int]
    IS_READY_FIELD_NUMBER: _ClassVar[int]
    LANGGRAPH_FIELD_NUMBER: _ClassVar[int]
    description: str
    framework: AgentFramework
    runtime: AgentRuntime
    icon_url: str
    git_repo: AgentGitRepo
    is_ready: bool
    langgraph: LangGraphConfig
    def __init__(self, description: _Optional[str] = ..., framework: _Optional[_Union[AgentFramework, str]] = ..., runtime: _Optional[_Union[AgentRuntime, str]] = ..., icon_url: _Optional[str] = ..., git_repo: _Optional[_Union[AgentGitRepo, _Mapping]] = ..., is_ready: bool = ..., langgraph: _Optional[_Union[LangGraphConfig, _Mapping]] = ...) -> None: ...

class AgentGitRepo(_message.Message):
    __slots__ = ("clone_url", "git_credential_id", "web_url", "overview_markdown_url", "readme_url", "branch", "commit_sha", "project_dir", "repo_path")
    CLONE_URL_FIELD_NUMBER: _ClassVar[int]
    GIT_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    WEB_URL_FIELD_NUMBER: _ClassVar[int]
    OVERVIEW_MARKDOWN_URL_FIELD_NUMBER: _ClassVar[int]
    README_URL_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    PROJECT_DIR_FIELD_NUMBER: _ClassVar[int]
    REPO_PATH_FIELD_NUMBER: _ClassVar[int]
    clone_url: str
    git_credential_id: str
    web_url: str
    overview_markdown_url: str
    readme_url: str
    branch: str
    commit_sha: str
    project_dir: str
    repo_path: str
    def __init__(self, clone_url: _Optional[str] = ..., git_credential_id: _Optional[str] = ..., web_url: _Optional[str] = ..., overview_markdown_url: _Optional[str] = ..., readme_url: _Optional[str] = ..., branch: _Optional[str] = ..., commit_sha: _Optional[str] = ..., project_dir: _Optional[str] = ..., repo_path: _Optional[str] = ...) -> None: ...

class LangGraphConfig(_message.Message):
    __slots__ = ("endpoint_url", "graph_name")
    ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    GRAPH_NAME_FIELD_NUMBER: _ClassVar[int]
    endpoint_url: str
    graph_name: str
    def __init__(self, endpoint_url: _Optional[str] = ..., graph_name: _Optional[str] = ...) -> None: ...
