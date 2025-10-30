from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpVpcRoutingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REGIONAL: _ClassVar[GcpVpcRoutingMode]
    GLOBAL: _ClassVar[GcpVpcRoutingMode]
REGIONAL: GcpVpcRoutingMode
GLOBAL: GcpVpcRoutingMode

class GcpVpcSpec(_message.Message):
    __slots__ = ("project_id", "auto_create_subnetworks", "routing_mode")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    AUTO_CREATE_SUBNETWORKS_FIELD_NUMBER: _ClassVar[int]
    ROUTING_MODE_FIELD_NUMBER: _ClassVar[int]
    project_id: _foreign_key_pb2.StringValueOrRef
    auto_create_subnetworks: bool
    routing_mode: GcpVpcRoutingMode
    def __init__(self, project_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., auto_create_subnetworks: bool = ..., routing_mode: _Optional[_Union[GcpVpcRoutingMode, str]] = ...) -> None: ...
