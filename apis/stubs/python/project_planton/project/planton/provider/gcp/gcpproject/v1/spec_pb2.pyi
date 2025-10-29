from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpProjectParentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    gcp_project_parent_type_unspecified: _ClassVar[GcpProjectParentType]
    organization: _ClassVar[GcpProjectParentType]
    folder: _ClassVar[GcpProjectParentType]
gcp_project_parent_type_unspecified: GcpProjectParentType
organization: GcpProjectParentType
folder: GcpProjectParentType

class GcpProjectSpec(_message.Message):
    __slots__ = ("parent_type", "parent_id", "billing_account_id", "labels", "disable_default_network", "enabled_apis", "owner_member")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PARENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    BILLING_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_DEFAULT_NETWORK_FIELD_NUMBER: _ClassVar[int]
    ENABLED_APIS_FIELD_NUMBER: _ClassVar[int]
    OWNER_MEMBER_FIELD_NUMBER: _ClassVar[int]
    parent_type: GcpProjectParentType
    parent_id: str
    billing_account_id: str
    labels: _containers.ScalarMap[str, str]
    disable_default_network: bool
    enabled_apis: _containers.RepeatedScalarFieldContainer[str]
    owner_member: str
    def __init__(self, parent_type: _Optional[_Union[GcpProjectParentType, str]] = ..., parent_id: _Optional[str] = ..., billing_account_id: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ..., disable_default_network: bool = ..., enabled_apis: _Optional[_Iterable[str]] = ..., owner_member: _Optional[str] = ...) -> None: ...
