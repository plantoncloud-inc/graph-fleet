from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsRdsInstanceSpec(_message.Message):
    __slots__ = ("subnet_ids", "db_subnet_group_name", "security_group_ids", "engine", "engine_version", "instance_class", "allocated_storage_gb", "storage_encrypted", "kms_key_id", "username", "password", "port", "publicly_accessible", "multi_az", "parameter_group_name", "option_group_name")
    SUBNET_IDS_FIELD_NUMBER: _ClassVar[int]
    DB_SUBNET_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_CLASS_FIELD_NUMBER: _ClassVar[int]
    ALLOCATED_STORAGE_GB_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    KMS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    PUBLICLY_ACCESSIBLE_FIELD_NUMBER: _ClassVar[int]
    MULTI_AZ_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    OPTION_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    subnet_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    db_subnet_group_name: _foreign_key_pb2.StringValueOrRef
    security_group_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    engine: str
    engine_version: str
    instance_class: str
    allocated_storage_gb: int
    storage_encrypted: bool
    kms_key_id: _foreign_key_pb2.StringValueOrRef
    username: str
    password: str
    port: int
    publicly_accessible: bool
    multi_az: bool
    parameter_group_name: str
    option_group_name: str
    def __init__(self, subnet_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., db_subnet_group_name: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., security_group_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., engine: _Optional[str] = ..., engine_version: _Optional[str] = ..., instance_class: _Optional[str] = ..., allocated_storage_gb: _Optional[int] = ..., storage_encrypted: bool = ..., kms_key_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., port: _Optional[int] = ..., publicly_accessible: bool = ..., multi_az: bool = ..., parameter_group_name: _Optional[str] = ..., option_group_name: _Optional[str] = ...) -> None: ...
