from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEcsServiceSpec(_message.Message):
    __slots__ = ("cluster_arn", "container", "network", "iam", "alb")
    CLUSTER_ARN_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    IAM_FIELD_NUMBER: _ClassVar[int]
    ALB_FIELD_NUMBER: _ClassVar[int]
    cluster_arn: _foreign_key_pb2.StringValueOrRef
    container: AwsEcsServiceContainer
    network: AwsEcsServiceNetwork
    iam: AwsEcsServiceIam
    alb: AwsEcsServiceAlb
    def __init__(self, cluster_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., container: _Optional[_Union[AwsEcsServiceContainer, _Mapping]] = ..., network: _Optional[_Union[AwsEcsServiceNetwork, _Mapping]] = ..., iam: _Optional[_Union[AwsEcsServiceIam, _Mapping]] = ..., alb: _Optional[_Union[AwsEcsServiceAlb, _Mapping]] = ...) -> None: ...

class AwsEcsServiceContainer(_message.Message):
    __slots__ = ("image", "env", "port", "replicas", "cpu", "memory", "logging")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    LOGGING_FIELD_NUMBER: _ClassVar[int]
    image: AwsEcsServiceContainerImage
    env: AwsEcsServiceContainerEnv
    port: int
    replicas: int
    cpu: int
    memory: int
    logging: AwsEcsServiceContainerLogging
    def __init__(self, image: _Optional[_Union[AwsEcsServiceContainerImage, _Mapping]] = ..., env: _Optional[_Union[AwsEcsServiceContainerEnv, _Mapping]] = ..., port: _Optional[int] = ..., replicas: _Optional[int] = ..., cpu: _Optional[int] = ..., memory: _Optional[int] = ..., logging: _Optional[_Union[AwsEcsServiceContainerLogging, _Mapping]] = ...) -> None: ...

class AwsEcsServiceContainerLogging(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class AwsEcsServiceContainerImage(_message.Message):
    __slots__ = ("repo", "tag")
    REPO_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    repo: str
    tag: str
    def __init__(self, repo: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class AwsEcsServiceContainerEnv(_message.Message):
    __slots__ = ("variables", "secrets", "s3_files")
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
    S3_FILES_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.ScalarMap[str, str]
    secrets: _containers.ScalarMap[str, str]
    s3_files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, variables: _Optional[_Mapping[str, str]] = ..., secrets: _Optional[_Mapping[str, str]] = ..., s3_files: _Optional[_Iterable[str]] = ...) -> None: ...

class AwsEcsServiceNetwork(_message.Message):
    __slots__ = ("subnets", "security_groups")
    SUBNETS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUPS_FIELD_NUMBER: _ClassVar[int]
    subnets: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    security_groups: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    def __init__(self, subnets: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., security_groups: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ...) -> None: ...

class AwsEcsServiceIam(_message.Message):
    __slots__ = ("task_execution_role_arn", "task_role_arn")
    TASK_EXECUTION_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    TASK_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    task_execution_role_arn: _foreign_key_pb2.StringValueOrRef
    task_role_arn: _foreign_key_pb2.StringValueOrRef
    def __init__(self, task_execution_role_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., task_role_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ...) -> None: ...

class AwsEcsServiceAlb(_message.Message):
    __slots__ = ("enabled", "arn", "routing_type", "path", "hostname", "listener_port", "listener_priority", "health_check")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ARN_FIELD_NUMBER: _ClassVar[int]
    ROUTING_TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    LISTENER_PORT_FIELD_NUMBER: _ClassVar[int]
    LISTENER_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    arn: _foreign_key_pb2.StringValueOrRef
    routing_type: str
    path: str
    hostname: str
    listener_port: int
    listener_priority: int
    health_check: AwsEcsServiceHealthCheck
    def __init__(self, enabled: bool = ..., arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., routing_type: _Optional[str] = ..., path: _Optional[str] = ..., hostname: _Optional[str] = ..., listener_port: _Optional[int] = ..., listener_priority: _Optional[int] = ..., health_check: _Optional[_Union[AwsEcsServiceHealthCheck, _Mapping]] = ...) -> None: ...

class AwsEcsServiceHealthCheck(_message.Message):
    __slots__ = ("protocol", "path", "port", "interval", "timeout", "healthy_threshold", "unhealthy_threshold")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    UNHEALTHY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    path: str
    port: str
    interval: int
    timeout: int
    healthy_threshold: int
    unhealthy_threshold: int
    def __init__(self, protocol: _Optional[str] = ..., path: _Optional[str] = ..., port: _Optional[str] = ..., interval: _Optional[int] = ..., timeout: _Optional[int] = ..., healthy_threshold: _Optional[int] = ..., unhealthy_threshold: _Optional[int] = ...) -> None: ...
