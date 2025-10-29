from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Architecture(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ARCHITECTURE_UNSPECIFIED: _ClassVar[Architecture]
    X86_64: _ClassVar[Architecture]
    ARM64: _ClassVar[Architecture]

class CodeSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CODE_SOURCE_TYPE_UNSPECIFIED: _ClassVar[CodeSourceType]
    CODE_SOURCE_TYPE_S3: _ClassVar[CodeSourceType]
    CODE_SOURCE_TYPE_IMAGE: _ClassVar[CodeSourceType]
ARCHITECTURE_UNSPECIFIED: Architecture
X86_64: Architecture
ARM64: Architecture
CODE_SOURCE_TYPE_UNSPECIFIED: CodeSourceType
CODE_SOURCE_TYPE_S3: CodeSourceType
CODE_SOURCE_TYPE_IMAGE: CodeSourceType

class AwsLambdaSpec(_message.Message):
    __slots__ = ("function_name", "description", "role_arn", "runtime", "handler", "memory_mb", "timeout_seconds", "reserved_concurrency", "environment", "subnets", "security_groups", "architecture", "layer_arns", "kms_key_arn", "code_source_type", "s3", "image_uri")
    class EnvironmentEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    HANDLER_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MB_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    RESERVED_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    SUBNETS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUPS_FIELD_NUMBER: _ClassVar[int]
    ARCHITECTURE_FIELD_NUMBER: _ClassVar[int]
    LAYER_ARNS_FIELD_NUMBER: _ClassVar[int]
    KMS_KEY_ARN_FIELD_NUMBER: _ClassVar[int]
    CODE_SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URI_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    description: str
    role_arn: _foreign_key_pb2.StringValueOrRef
    runtime: str
    handler: str
    memory_mb: int
    timeout_seconds: int
    reserved_concurrency: int
    environment: _containers.ScalarMap[str, str]
    subnets: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    security_groups: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    architecture: Architecture
    layer_arns: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    kms_key_arn: _foreign_key_pb2.StringValueOrRef
    code_source_type: CodeSourceType
    s3: S3Code
    image_uri: str
    def __init__(self, function_name: _Optional[str] = ..., description: _Optional[str] = ..., role_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., runtime: _Optional[str] = ..., handler: _Optional[str] = ..., memory_mb: _Optional[int] = ..., timeout_seconds: _Optional[int] = ..., reserved_concurrency: _Optional[int] = ..., environment: _Optional[_Mapping[str, str]] = ..., subnets: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., security_groups: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., architecture: _Optional[_Union[Architecture, str]] = ..., layer_arns: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., kms_key_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., code_source_type: _Optional[_Union[CodeSourceType, str]] = ..., s3: _Optional[_Union[S3Code, _Mapping]] = ..., image_uri: _Optional[str] = ...) -> None: ...

class S3Code(_message.Message):
    __slots__ = ("bucket", "key", "object_version")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    OBJECT_VERSION_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    key: str
    object_version: str
    def __init__(self, bucket: _Optional[str] = ..., key: _Optional[str] = ..., object_version: _Optional[str] = ...) -> None: ...
