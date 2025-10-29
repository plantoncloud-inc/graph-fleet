from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEksClusterSpec(_message.Message):
    __slots__ = ("subnet_ids", "cluster_role_arn", "version", "disable_public_endpoint", "public_access_cidrs", "enable_control_plane_logs", "kms_key_arn")
    SUBNET_IDS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DISABLE_PUBLIC_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_ACCESS_CIDRS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CONTROL_PLANE_LOGS_FIELD_NUMBER: _ClassVar[int]
    KMS_KEY_ARN_FIELD_NUMBER: _ClassVar[int]
    subnet_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    cluster_role_arn: _foreign_key_pb2.StringValueOrRef
    version: str
    disable_public_endpoint: bool
    public_access_cidrs: _containers.RepeatedScalarFieldContainer[str]
    enable_control_plane_logs: bool
    kms_key_arn: _foreign_key_pb2.StringValueOrRef
    def __init__(self, subnet_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., cluster_role_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., version: _Optional[str] = ..., disable_public_endpoint: bool = ..., public_access_cidrs: _Optional[_Iterable[str]] = ..., enable_control_plane_logs: bool = ..., kms_key_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ...) -> None: ...
