from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceGroup(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    api_resource_group_unspecified: _ClassVar[ApiResourceGroup]
    test: _ClassVar[ApiResourceGroup]
    audit: _ClassVar[ApiResourceGroup]
    billing: _ClassVar[ApiResourceGroup]
    infra_hub: _ClassVar[ApiResourceGroup]
    connect: _ClassVar[ApiResourceGroup]
    iam: _ClassVar[ApiResourceGroup]
    copilot: _ClassVar[ApiResourceGroup]
    resource_manager: _ClassVar[ApiResourceGroup]
    service_hub: _ClassVar[ApiResourceGroup]
    project_planton_credential: _ClassVar[ApiResourceGroup]
    secrets_manager: _ClassVar[ApiResourceGroup]
    agent_fleet: _ClassVar[ApiResourceGroup]
api_resource_group_unspecified: ApiResourceGroup
test: ApiResourceGroup
audit: ApiResourceGroup
billing: ApiResourceGroup
infra_hub: ApiResourceGroup
connect: ApiResourceGroup
iam: ApiResourceGroup
copilot: ApiResourceGroup
resource_manager: ApiResourceGroup
service_hub: ApiResourceGroup
project_planton_credential: ApiResourceGroup
secrets_manager: ApiResourceGroup
agent_fleet: ApiResourceGroup
GROUP_META_FIELD_NUMBER: _ClassVar[int]
group_meta: _descriptor.FieldDescriptor

class ApiResourceGroupMeta(_message.Message):
    __slots__ = ("domain", "display_name", "is_project_planton_group")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_PROJECT_PLANTON_GROUP_FIELD_NUMBER: _ClassVar[int]
    domain: str
    display_name: str
    is_project_planton_group: bool
    def __init__(self, domain: _Optional[str] = ..., display_name: _Optional[str] = ..., is_project_planton_group: bool = ...) -> None: ...
