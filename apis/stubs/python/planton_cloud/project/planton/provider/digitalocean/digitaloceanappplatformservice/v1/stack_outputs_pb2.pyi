from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanAppPlatformServiceStackOutputs(_message.Message):
    __slots__ = ("app_id", "default_hostname", "live_url")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    LIVE_URL_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    default_hostname: str
    live_url: str
    def __init__(self, app_id: _Optional[str] = ..., default_hostname: _Optional[str] = ..., live_url: _Optional[str] = ...) -> None: ...
