from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoBucketStackOutputs(_message.Message):
    __slots__ = ("bucket_id", "endpoint_url", "access_key_secret_ref", "secret_key_secret_ref")
    BUCKET_ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_SECRET_REF_FIELD_NUMBER: _ClassVar[int]
    SECRET_KEY_SECRET_REF_FIELD_NUMBER: _ClassVar[int]
    bucket_id: str
    endpoint_url: str
    access_key_secret_ref: str
    secret_key_secret_ref: str
    def __init__(self, bucket_id: _Optional[str] = ..., endpoint_url: _Optional[str] = ..., access_key_secret_ref: _Optional[str] = ..., secret_key_secret_ref: _Optional[str] = ...) -> None: ...
