from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CertManagerKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "release_name", "solver_identity")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    RELEASE_NAME_FIELD_NUMBER: _ClassVar[int]
    SOLVER_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    release_name: str
    solver_identity: str
    def __init__(self, namespace: _Optional[str] = ..., release_name: _Optional[str] = ..., solver_identity: _Optional[str] = ...) -> None: ...
