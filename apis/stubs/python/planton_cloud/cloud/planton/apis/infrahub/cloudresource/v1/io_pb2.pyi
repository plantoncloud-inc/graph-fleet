from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.infrahub.cloudresource.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.infrahub.cloudresource.v1 import mutator_pb2 as _mutator_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class CloudResourceKindRequest(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _cloud_resource_kind_pb2.CloudResourceKind
    def __init__(self, value: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ...) -> None: ...

class CloudResourceByOrgByEnvByKindBySlugRequest(_message.Message):
    __slots__ = ("org", "env", "cloud_resource_kind", "slug")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    slug: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., slug: _Optional[str] = ...) -> None: ...

class ResolveValueFromReferencesRequest(_message.Message):
    __slots__ = ("cloud_resource_kind", "cloud_resource_id")
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    cloud_resource_id: str
    def __init__(self, cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., cloud_resource_id: _Optional[str] = ...) -> None: ...

class ResolveValueFromReferencesResponse(_message.Message):
    __slots__ = ("is_resolved", "errors", "diagnostics", "cloud_resource_yaml")
    IS_RESOLVED_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_YAML_FIELD_NUMBER: _ClassVar[int]
    is_resolved: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    diagnostics: _containers.RepeatedScalarFieldContainer[str]
    cloud_resource_yaml: str
    def __init__(self, is_resolved: bool = ..., errors: _Optional[_Iterable[str]] = ..., diagnostics: _Optional[_Iterable[str]] = ..., cloud_resource_yaml: _Optional[str] = ...) -> None: ...

class GetCloudResourcesGraphViewRequest(_message.Message):
    __slots__ = ("org", "envs", "search_text", "kinds")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENVS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    KINDS_FIELD_NUMBER: _ClassVar[int]
    org: str
    envs: _containers.RepeatedScalarFieldContainer[str]
    search_text: str
    kinds: _containers.RepeatedScalarFieldContainer[_cloud_resource_kind_pb2.CloudResourceKind]
    def __init__(self, org: _Optional[str] = ..., envs: _Optional[_Iterable[str]] = ..., search_text: _Optional[str] = ..., kinds: _Optional[_Iterable[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]]] = ...) -> None: ...

class RenameCloudResourceRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateCloudResourceOutputsRequest(_message.Message):
    __slots__ = ("cloud_resource_id", "outputs")
    class OutputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CLOUD_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_id: str
    outputs: _containers.ScalarMap[str, str]
    def __init__(self, cloud_resource_id: _Optional[str] = ..., outputs: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CloudResourcePipelineOperationRequest(_message.Message):
    __slots__ = ("cloud_resource", "mutator")
    CLOUD_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    MUTATOR_FIELD_NUMBER: _ClassVar[int]
    cloud_resource: _api_pb2.CloudResource
    mutator: _mutator_pb2.CloudResourceMutator
    def __init__(self, cloud_resource: _Optional[_Union[_api_pb2.CloudResource, _Mapping]] = ..., mutator: _Optional[_Union[_mutator_pb2.CloudResourceMutator, _Mapping]] = ...) -> None: ...

class CloudResourceList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.CloudResource]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_api_pb2.CloudResource, _Mapping]]] = ...) -> None: ...
