from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoVolumeStackOutputs(_message.Message):
    __slots__ = ("volume_id", "attached_instance_id", "device_path")
    VOLUME_ID_FIELD_NUMBER: _ClassVar[int]
    ATTACHED_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_PATH_FIELD_NUMBER: _ClassVar[int]
    volume_id: str
    attached_instance_id: str
    device_path: str
    def __init__(self, volume_id: _Optional[str] = ..., attached_instance_id: _Optional[str] = ..., device_path: _Optional[str] = ...) -> None: ...
