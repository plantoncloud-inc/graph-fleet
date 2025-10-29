from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuickActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    quick_action_type_unspecified: _ClassVar[QuickActionType]
    create: _ClassVar[QuickActionType]
    list: _ClassVar[QuickActionType]
quick_action_type_unspecified: QuickActionType
create: QuickActionType
list: QuickActionType

class QuickActionSpec(_message.Message):
    __slots__ = ("api_resource_kind", "cloud_resource_kind", "action_type", "icon_url", "is_ready")
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    IS_READY_FIELD_NUMBER: _ClassVar[int]
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    action_type: QuickActionType
    icon_url: str
    is_ready: bool
    def __init__(self, api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., action_type: _Optional[_Union[QuickActionType, str]] = ..., icon_url: _Optional[str] = ..., is_ready: bool = ...) -> None: ...
