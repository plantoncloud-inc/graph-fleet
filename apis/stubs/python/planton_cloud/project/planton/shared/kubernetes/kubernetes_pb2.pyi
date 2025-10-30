from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Container(_message.Message):
    __slots__ = ("name", "image", "ports", "resources", "env")
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    name: str
    image: str
    ports: _containers.RepeatedCompositeFieldContainer[ContainerPort]
    resources: ContainerResources
    env: _containers.RepeatedCompositeFieldContainer[ContainerEnvVar]
    def __init__(self, name: _Optional[str] = ..., image: _Optional[str] = ..., ports: _Optional[_Iterable[_Union[ContainerPort, _Mapping]]] = ..., resources: _Optional[_Union[ContainerResources, _Mapping]] = ..., env: _Optional[_Iterable[_Union[ContainerEnvVar, _Mapping]]] = ...) -> None: ...

class ContainerResources(_message.Message):
    __slots__ = ("limits", "requests")
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    limits: CpuMemory
    requests: CpuMemory
    def __init__(self, limits: _Optional[_Union[CpuMemory, _Mapping]] = ..., requests: _Optional[_Union[CpuMemory, _Mapping]] = ...) -> None: ...

class ContainerEnvVar(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class ContainerPort(_message.Message):
    __slots__ = ("name", "container_port", "protocol")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    name: str
    container_port: int
    protocol: str
    def __init__(self, name: _Optional[str] = ..., container_port: _Optional[int] = ..., protocol: _Optional[str] = ...) -> None: ...

class CpuMemory(_message.Message):
    __slots__ = ("cpu", "memory")
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    cpu: str
    memory: str
    def __init__(self, cpu: _Optional[str] = ..., memory: _Optional[str] = ...) -> None: ...

class ContainerImage(_message.Message):
    __slots__ = ("repo", "tag", "pull_secret_name")
    REPO_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    PULL_SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    repo: str
    tag: str
    pull_secret_name: str
    def __init__(self, repo: _Optional[str] = ..., tag: _Optional[str] = ..., pull_secret_name: _Optional[str] = ...) -> None: ...

class IngressSpec(_message.Message):
    __slots__ = ("enabled", "dns_domain")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DNS_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    dns_domain: str
    def __init__(self, enabled: bool = ..., dns_domain: _Optional[str] = ...) -> None: ...

class KubernetesSecretKey(_message.Message):
    __slots__ = ("name", "key")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    name: str
    key: str
    def __init__(self, name: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...
