from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.iam.iamrole.v1 import api_pb2 as _api_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IamRoleId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class IamApiResourceKindInput(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class IamRoles(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.IamRole]
    def __init__(self, entries: _Optional[_Iterable[_Union[_api_pb2.IamRole, _Mapping]]] = ...) -> None: ...

class IamRoleList(_message.Message):
    __slots__ = ("entries", "total_pages")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.IamRole]
    total_pages: int
    def __init__(self, entries: _Optional[_Iterable[_Union[_api_pb2.IamRole, _Mapping]]] = ..., total_pages: _Optional[int] = ...) -> None: ...

class ApiResourceKindAndPrincipalTypeInput(_message.Message):
    __slots__ = ("resource_kind", "principal_type")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    resource_kind: str
    principal_type: str
    def __init__(self, resource_kind: _Optional[str] = ..., principal_type: _Optional[str] = ...) -> None: ...

class PrincipalTypes(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entries: _Optional[_Iterable[str]] = ...) -> None: ...
