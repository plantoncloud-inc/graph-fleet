from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpCloudRunSpec(_message.Message):
    __slots__ = ("project_id", "region", "container", "max_concurrency", "allow_unauthenticated", "dns")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    MAX_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    ALLOW_UNAUTHENTICATED_FIELD_NUMBER: _ClassVar[int]
    DNS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    region: str
    container: GcpCloudRunContainer
    max_concurrency: int
    allow_unauthenticated: bool
    dns: GcpCloudRunDns
    def __init__(self, project_id: _Optional[str] = ..., region: _Optional[str] = ..., container: _Optional[_Union[GcpCloudRunContainer, _Mapping]] = ..., max_concurrency: _Optional[int] = ..., allow_unauthenticated: bool = ..., dns: _Optional[_Union[GcpCloudRunDns, _Mapping]] = ...) -> None: ...

class GcpCloudRunContainer(_message.Message):
    __slots__ = ("image", "env", "port", "cpu", "memory", "replicas")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    image: GcpCloudRunContainerImage
    env: GcpCloudRunContainerEnv
    port: int
    cpu: int
    memory: int
    replicas: GcpCloudRunContainerReplicas
    def __init__(self, image: _Optional[_Union[GcpCloudRunContainerImage, _Mapping]] = ..., env: _Optional[_Union[GcpCloudRunContainerEnv, _Mapping]] = ..., port: _Optional[int] = ..., cpu: _Optional[int] = ..., memory: _Optional[int] = ..., replicas: _Optional[_Union[GcpCloudRunContainerReplicas, _Mapping]] = ...) -> None: ...

class GcpCloudRunContainerReplicas(_message.Message):
    __slots__ = ("min", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: int
    max: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class GcpCloudRunContainerImage(_message.Message):
    __slots__ = ("repo", "tag")
    REPO_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    repo: str
    tag: str
    def __init__(self, repo: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class GcpCloudRunContainerEnv(_message.Message):
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

class GcpCloudRunDns(_message.Message):
    __slots__ = ("enabled", "hostnames", "managed_zone")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTNAMES_FIELD_NUMBER: _ClassVar[int]
    MANAGED_ZONE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    hostnames: _containers.RepeatedScalarFieldContainer[str]
    managed_zone: str
    def __init__(self, enabled: bool = ..., hostnames: _Optional[_Iterable[str]] = ..., managed_zone: _Optional[str] = ...) -> None: ...
