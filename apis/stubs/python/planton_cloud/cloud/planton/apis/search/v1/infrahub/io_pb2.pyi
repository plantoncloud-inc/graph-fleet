from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_provider_pb2 as _cloud_resource_provider_pb2
from project.planton.shared import iac_pb2 as _iac_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchDeploymentComponentsByFilterInput(_message.Message):
    __slots__ = ("search_text", "page_info", "providers")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    page_info: _pagination_pb2.PageInfo
    providers: _containers.RepeatedScalarFieldContainer[_cloud_resource_provider_pb2.CloudResourceProvider]
    def __init__(self, search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., providers: _Optional[_Iterable[_Union[_cloud_resource_provider_pb2.CloudResourceProvider, str]]] = ...) -> None: ...

class SearchPulumiModuleByTextInput(_message.Message):
    __slots__ = ("search_text", "page_info")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    page_info: _pagination_pb2.PageInfo
    def __init__(self, search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ...) -> None: ...

class SearchIacModulesByOrgContextInput(_message.Message):
    __slots__ = ("search_text", "page_info", "org", "provisioners", "cloud_resource_kind", "is_include_official", "is_include_organization_modules", "providers")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    PROVISIONERS_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_OFFICIAL_FIELD_NUMBER: _ClassVar[int]
    IS_INCLUDE_ORGANIZATION_MODULES_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    page_info: _pagination_pb2.PageInfo
    org: str
    provisioners: _containers.RepeatedScalarFieldContainer[_iac_pb2.IacProvisioner]
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    is_include_official: bool
    is_include_organization_modules: bool
    providers: _containers.RepeatedScalarFieldContainer[_cloud_resource_provider_pb2.CloudResourceProvider]
    def __init__(self, search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., org: _Optional[str] = ..., provisioners: _Optional[_Iterable[_Union[_iac_pb2.IacProvisioner, str]]] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., is_include_official: bool = ..., is_include_organization_modules: bool = ..., providers: _Optional[_Iterable[_Union[_cloud_resource_provider_pb2.CloudResourceProvider, str]]] = ...) -> None: ...

class SearchOfficialIacModulesInput(_message.Message):
    __slots__ = ("search_text", "page_info", "cloud_resource_kind", "provisioners", "providers")
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    PROVISIONERS_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    search_text: str
    page_info: _pagination_pb2.PageInfo
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    provisioners: _containers.RepeatedScalarFieldContainer[_iac_pb2.IacProvisioner]
    providers: _containers.RepeatedScalarFieldContainer[_cloud_resource_provider_pb2.CloudResourceProvider]
    def __init__(self, search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., provisioners: _Optional[_Iterable[_Union[_iac_pb2.IacProvisioner, str]]] = ..., providers: _Optional[_Iterable[_Union[_cloud_resource_provider_pb2.CloudResourceProvider, str]]] = ...) -> None: ...

class FindDeploymentComponentIacModulesByOrgContextInput(_message.Message):
    __slots__ = ("page_info", "org", "deployment_component_resource_kind")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_COMPONENT_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    org: str
    deployment_component_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., org: _Optional[str] = ..., deployment_component_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ...) -> None: ...
