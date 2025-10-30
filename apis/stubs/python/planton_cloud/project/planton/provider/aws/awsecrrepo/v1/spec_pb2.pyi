from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEcrRepoSpec(_message.Message):
    __slots__ = ("repository_name", "image_immutable", "encryption_type", "kms_key_id", "force_delete")
    REPOSITORY_NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_IMMUTABLE_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    KMS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_DELETE_FIELD_NUMBER: _ClassVar[int]
    repository_name: str
    image_immutable: bool
    encryption_type: str
    kms_key_id: str
    force_delete: bool
    def __init__(self, repository_name: _Optional[str] = ..., image_immutable: bool = ..., encryption_type: _Optional[str] = ..., kms_key_id: _Optional[str] = ..., force_delete: bool = ...) -> None: ...
