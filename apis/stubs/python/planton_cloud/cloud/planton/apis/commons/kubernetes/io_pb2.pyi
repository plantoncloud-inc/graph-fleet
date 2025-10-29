from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class KubeConfigAndNamespace(_message.Message):
    __slots__ = ("kube_config_base64", "namespace")
    KUBE_CONFIG_BASE64_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    kube_config_base64: str
    namespace: str
    def __init__(self, kube_config_base64: _Optional[str] = ..., namespace: _Optional[str] = ...) -> None: ...
