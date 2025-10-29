from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_provider_pb2 as _cloud_resource_provider_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentComponentSpec(_message.Message):
    __slots__ = ("cloud_resource_kind", "description", "provider", "provider_icon_url", "icon_url", "web_links", "is_ready")
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ICON_URL_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    WEB_LINKS_FIELD_NUMBER: _ClassVar[int]
    IS_READY_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    description: str
    provider: _cloud_resource_provider_pb2.CloudResourceProvider
    provider_icon_url: str
    icon_url: str
    web_links: DeploymentComponentWebLinks
    is_ready: bool
    def __init__(self, cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., description: _Optional[str] = ..., provider: _Optional[_Union[_cloud_resource_provider_pb2.CloudResourceProvider, str]] = ..., provider_icon_url: _Optional[str] = ..., icon_url: _Optional[str] = ..., web_links: _Optional[_Union[DeploymentComponentWebLinks, _Mapping]] = ..., is_ready: bool = ...) -> None: ...

class DeploymentComponentWebLinks(_message.Message):
    __slots__ = ("api", "overview_markdown_url", "example_markdown_url")
    API_FIELD_NUMBER: _ClassVar[int]
    OVERVIEW_MARKDOWN_URL_FIELD_NUMBER: _ClassVar[int]
    EXAMPLE_MARKDOWN_URL_FIELD_NUMBER: _ClassVar[int]
    api: DeploymentComponentApiWebLinks
    overview_markdown_url: str
    example_markdown_url: str
    def __init__(self, api: _Optional[_Union[DeploymentComponentApiWebLinks, _Mapping]] = ..., overview_markdown_url: _Optional[str] = ..., example_markdown_url: _Optional[str] = ...) -> None: ...

class DeploymentComponentApiWebLinks(_message.Message):
    __slots__ = ("source_code", "documentation")
    SOURCE_CODE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    source_code: DeploymentComponentApiSourceCodeWebLinks
    documentation: DeploymentComponentApiDocumentationWebLinks
    def __init__(self, source_code: _Optional[_Union[DeploymentComponentApiSourceCodeWebLinks, _Mapping]] = ..., documentation: _Optional[_Union[DeploymentComponentApiDocumentationWebLinks, _Mapping]] = ...) -> None: ...

class DeploymentComponentApiSourceCodeWebLinks(_message.Message):
    __slots__ = ("root", "spec", "stack_input", "stack_outputs")
    ROOT_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STACK_INPUT_FIELD_NUMBER: _ClassVar[int]
    STACK_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    root: str
    spec: str
    stack_input: str
    stack_outputs: str
    def __init__(self, root: _Optional[str] = ..., spec: _Optional[str] = ..., stack_input: _Optional[str] = ..., stack_outputs: _Optional[str] = ...) -> None: ...

class DeploymentComponentApiDocumentationWebLinks(_message.Message):
    __slots__ = ("root", "spec", "stack_input", "stack_outputs")
    ROOT_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STACK_INPUT_FIELD_NUMBER: _ClassVar[int]
    STACK_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    root: str
    spec: str
    stack_input: str
    stack_outputs: str
    def __init__(self, root: _Optional[str] = ..., spec: _Optional[str] = ..., stack_input: _Optional[str] = ..., stack_outputs: _Optional[str] = ...) -> None: ...
