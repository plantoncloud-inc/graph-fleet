from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.digitalocean import region_pb2 as _region_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanProviderConfig(_message.Message):
    __slots__ = ("api_token", "default_region", "spaces_access_id", "spaces_secret_key")
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REGION_FIELD_NUMBER: _ClassVar[int]
    SPACES_ACCESS_ID_FIELD_NUMBER: _ClassVar[int]
    SPACES_SECRET_KEY_FIELD_NUMBER: _ClassVar[int]
    api_token: str
    default_region: _region_pb2.DigitalOceanRegion
    spaces_access_id: str
    spaces_secret_key: str
    def __init__(self, api_token: _Optional[str] = ..., default_region: _Optional[_Union[_region_pb2.DigitalOceanRegion, str]] = ..., spaces_access_id: _Optional[str] = ..., spaces_secret_key: _Optional[str] = ...) -> None: ...
