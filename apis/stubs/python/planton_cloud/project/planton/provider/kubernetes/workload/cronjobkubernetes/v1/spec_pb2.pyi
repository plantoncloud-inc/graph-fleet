from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from project.planton.shared.kubernetes import options_pb2 as _options_pb2
from project.planton.shared.options import options_pb2 as _options_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CronJobKubernetesSpec(_message.Message):
    __slots__ = ("image", "resources", "env", "schedule", "starting_deadline_seconds", "concurrency_policy", "suspend", "successful_jobs_history_limit", "failed_jobs_history_limit", "backoff_limit", "restart_policy", "command", "args")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    STARTING_DEADLINE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONCURRENCY_POLICY_FIELD_NUMBER: _ClassVar[int]
    SUSPEND_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_JOBS_HISTORY_LIMIT_FIELD_NUMBER: _ClassVar[int]
    FAILED_JOBS_HISTORY_LIMIT_FIELD_NUMBER: _ClassVar[int]
    BACKOFF_LIMIT_FIELD_NUMBER: _ClassVar[int]
    RESTART_POLICY_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    image: _kubernetes_pb2.ContainerImage
    resources: _kubernetes_pb2.ContainerResources
    env: CronJobKubernetesContainerAppEnv
    schedule: str
    starting_deadline_seconds: int
    concurrency_policy: str
    suspend: bool
    successful_jobs_history_limit: int
    failed_jobs_history_limit: int
    backoff_limit: int
    restart_policy: str
    command: _containers.RepeatedScalarFieldContainer[str]
    args: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, image: _Optional[_Union[_kubernetes_pb2.ContainerImage, _Mapping]] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., env: _Optional[_Union[CronJobKubernetesContainerAppEnv, _Mapping]] = ..., schedule: _Optional[str] = ..., starting_deadline_seconds: _Optional[int] = ..., concurrency_policy: _Optional[str] = ..., suspend: bool = ..., successful_jobs_history_limit: _Optional[int] = ..., failed_jobs_history_limit: _Optional[int] = ..., backoff_limit: _Optional[int] = ..., restart_policy: _Optional[str] = ..., command: _Optional[_Iterable[str]] = ..., args: _Optional[_Iterable[str]] = ...) -> None: ...

class CronJobKubernetesContainerAppEnv(_message.Message):
    __slots__ = ("variables", "secrets")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SecretsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.ScalarMap[str, str]
    secrets: _containers.ScalarMap[str, str]
    def __init__(self, variables: _Optional[_Mapping[str, str]] = ..., secrets: _Optional[_Mapping[str, str]] = ...) -> None: ...
