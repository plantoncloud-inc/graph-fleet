from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanAppPlatformServiceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    digital_ocean_app_platform_service_type_unspecified: _ClassVar[DigitalOceanAppPlatformServiceType]
    web_service: _ClassVar[DigitalOceanAppPlatformServiceType]
    worker: _ClassVar[DigitalOceanAppPlatformServiceType]
    job: _ClassVar[DigitalOceanAppPlatformServiceType]

class DigitalOceanAppPlatformInstanceSize(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    digital_ocean_app_platform_instance_size_unspecified: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    basic_xxs: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    basic_xs: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    basic_s: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    basic_m: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    basic_l: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    professional_xs: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    professional_s: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    professional_m: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    professional_l: _ClassVar[DigitalOceanAppPlatformInstanceSize]
    professional_xl: _ClassVar[DigitalOceanAppPlatformInstanceSize]
digital_ocean_app_platform_service_type_unspecified: DigitalOceanAppPlatformServiceType
web_service: DigitalOceanAppPlatformServiceType
worker: DigitalOceanAppPlatformServiceType
job: DigitalOceanAppPlatformServiceType
digital_ocean_app_platform_instance_size_unspecified: DigitalOceanAppPlatformInstanceSize
basic_xxs: DigitalOceanAppPlatformInstanceSize
basic_xs: DigitalOceanAppPlatformInstanceSize
basic_s: DigitalOceanAppPlatformInstanceSize
basic_m: DigitalOceanAppPlatformInstanceSize
basic_l: DigitalOceanAppPlatformInstanceSize
professional_xs: DigitalOceanAppPlatformInstanceSize
professional_s: DigitalOceanAppPlatformInstanceSize
professional_m: DigitalOceanAppPlatformInstanceSize
professional_l: DigitalOceanAppPlatformInstanceSize
professional_xl: DigitalOceanAppPlatformInstanceSize

class DigitalOceanAppPlatformServiceSpec(_message.Message):
    __slots__ = ("service_name", "region", "service_type", "git_source", "image_source", "instance_size_slug", "instance_count", "enable_autoscale", "min_instance_count", "max_instance_count", "env", "custom_domain")
    class EnvEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    GIT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_SIZE_SLUG_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    ENABLE_AUTOSCALE_FIELD_NUMBER: _ClassVar[int]
    MIN_INSTANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_INSTANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    region: _region_pb2.DigitalOceanRegion
    service_type: DigitalOceanAppPlatformServiceType
    git_source: DigitalOceanAppPlatformGitSource
    image_source: DigitalOceanAppPlatformRegistrySource
    instance_size_slug: DigitalOceanAppPlatformInstanceSize
    instance_count: int
    enable_autoscale: bool
    min_instance_count: int
    max_instance_count: int
    env: _containers.ScalarMap[str, str]
    custom_domain: _foreign_key_pb2.StringValueOrRef
    def __init__(self, service_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., service_type: _Optional[_Union[DigitalOceanAppPlatformServiceType, str]] = ..., git_source: _Optional[_Union[DigitalOceanAppPlatformGitSource, _Mapping]] = ..., image_source: _Optional[_Union[DigitalOceanAppPlatformRegistrySource, _Mapping]] = ..., instance_size_slug: _Optional[_Union[DigitalOceanAppPlatformInstanceSize, str]] = ..., instance_count: _Optional[int] = ..., enable_autoscale: bool = ..., min_instance_count: _Optional[int] = ..., max_instance_count: _Optional[int] = ..., env: _Optional[_Mapping[str, str]] = ..., custom_domain: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ...) -> None: ...

class DigitalOceanAppPlatformGitSource(_message.Message):
    __slots__ = ("repo_url", "branch", "build_command", "run_command")
    REPO_URL_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    BUILD_COMMAND_FIELD_NUMBER: _ClassVar[int]
    RUN_COMMAND_FIELD_NUMBER: _ClassVar[int]
    repo_url: str
    branch: str
    build_command: str
    run_command: str
    def __init__(self, repo_url: _Optional[str] = ..., branch: _Optional[str] = ..., build_command: _Optional[str] = ..., run_command: _Optional[str] = ...) -> None: ...

class DigitalOceanAppPlatformRegistrySource(_message.Message):
    __slots__ = ("registry", "repository", "tag")
    REGISTRY_FIELD_NUMBER: _ClassVar[int]
    REPOSITORY_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    registry: _foreign_key_pb2.StringValueOrRef
    repository: str
    tag: str
    def __init__(self, registry: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., repository: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...
