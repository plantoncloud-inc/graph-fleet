from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IngressNginxKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "release_name", "service_name", "service_type")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    RELEASE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    release_name: str
    service_name: str
    service_type: str
    def __init__(self, namespace: _Optional[str] = ..., release_name: _Optional[str] = ..., service_name: _Optional[str] = ..., service_type: _Optional[str] = ...) -> None: ...
