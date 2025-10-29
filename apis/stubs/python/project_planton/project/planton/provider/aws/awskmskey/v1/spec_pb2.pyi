from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsKmsKeyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    symmetric: _ClassVar[AwsKmsKeyType]
    rsa_2048: _ClassVar[AwsKmsKeyType]
    rsa_4096: _ClassVar[AwsKmsKeyType]
    ecc_nist_p256: _ClassVar[AwsKmsKeyType]
symmetric: AwsKmsKeyType
rsa_2048: AwsKmsKeyType
rsa_4096: AwsKmsKeyType
ecc_nist_p256: AwsKmsKeyType

class AwsKmsKeySpec(_message.Message):
    __slots__ = ("key_spec", "description", "disable_key_rotation", "deletion_window_days", "alias_name")
    KEY_SPEC_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISABLE_KEY_ROTATION_FIELD_NUMBER: _ClassVar[int]
    DELETION_WINDOW_DAYS_FIELD_NUMBER: _ClassVar[int]
    ALIAS_NAME_FIELD_NUMBER: _ClassVar[int]
    key_spec: AwsKmsKeyType
    description: str
    disable_key_rotation: bool
    deletion_window_days: int
    alias_name: str
    def __init__(self, key_spec: _Optional[_Union[AwsKmsKeyType, str]] = ..., description: _Optional[str] = ..., disable_key_rotation: bool = ..., deletion_window_days: _Optional[int] = ..., alias_name: _Optional[str] = ...) -> None: ...
