from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ExternalDnsKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "release_name", "solver_sa")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    RELEASE_NAME_FIELD_NUMBER: _ClassVar[int]
    SOLVER_SA_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    release_name: str
    solver_sa: str
    def __init__(self, namespace: _Optional[str] = ..., release_name: _Optional[str] = ..., solver_sa: _Optional[str] = ...) -> None: ...
