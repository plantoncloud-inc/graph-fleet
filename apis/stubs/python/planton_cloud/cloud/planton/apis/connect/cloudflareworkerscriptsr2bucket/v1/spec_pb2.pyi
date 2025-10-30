from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudflareWorkerScriptsR2BucketSpec(_message.Message):
    __slots__ = ("bucket_name", "account_id", "endpoint_url", "access_key_id", "secret_access_key")
    BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    bucket_name: str
    account_id: str
    endpoint_url: str
    access_key_id: str
    secret_access_key: str
    def __init__(self, bucket_name: _Optional[str] = ..., account_id: _Optional[str] = ..., endpoint_url: _Optional[str] = ..., access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ...) -> None: ...
