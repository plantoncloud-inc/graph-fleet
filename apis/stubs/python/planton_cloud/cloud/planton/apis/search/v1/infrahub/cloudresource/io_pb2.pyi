from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import io_pb2 as _io_pb2
from cloud.planton.apis.search.v1.apiresource import io_pb2 as _io_pb2_1
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_provider_pb2 as _cloud_resource_provider_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExploreCloudResourcesRequest(_message.Message):
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

class ExploreCloudResourcesCanvasViewResponse(_message.Message):
    __slots__ = ("canvas_environments",)
    CANVAS_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    canvas_environments: _containers.RepeatedCompositeFieldContainer[CanvasEnvironment]
    def __init__(self, canvas_environments: _Optional[_Iterable[_Union[CanvasEnvironment, _Mapping]]] = ...) -> None: ...

class CanvasEnvironment(_message.Message):
    __slots__ = ("env_id", "env_slug", "resource_kind_mapping")
    class ResourceKindMappingEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _io_pb2_1.ApiResourceSearchRecords
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_io_pb2_1.ApiResourceSearchRecords, _Mapping]] = ...) -> None: ...
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    ENV_SLUG_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_KIND_MAPPING_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    env_slug: str
    resource_kind_mapping: _containers.MessageMap[str, _io_pb2_1.ApiResourceSearchRecords]
    def __init__(self, env_id: _Optional[str] = ..., env_slug: _Optional[str] = ..., resource_kind_mapping: _Optional[_Mapping[str, _io_pb2_1.ApiResourceSearchRecords]] = ...) -> None: ...

class LookupCloudResourceInput(_message.Message):
    __slots__ = ("org", "env", "cloud_resource_kind", "name")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    name: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., name: _Optional[str] = ...) -> None: ...

class CloudResourceCountsGroupedByKind(_message.Message):
    __slots__ = ("counts",)
    COUNTS_FIELD_NUMBER: _ClassVar[int]
    counts: _containers.RepeatedCompositeFieldContainer[CloudResourceKindCount]
    def __init__(self, counts: _Optional[_Iterable[_Union[CloudResourceKindCount, _Mapping]]] = ...) -> None: ...

class CloudResourceKindCount(_message.Message):
    __slots__ = ("kind", "count")
    KIND_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    kind: _cloud_resource_kind_pb2.CloudResourceKind
    count: int
    def __init__(self, kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., count: _Optional[int] = ...) -> None: ...

class GetCloudResourceCountsGroupedByKindInput(_message.Message):
    __slots__ = ("owner", "search_kind", "providers")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SEARCH_KIND_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    owner: _io_pb2.CloudResourceOwner
    search_kind: str
    providers: _containers.RepeatedScalarFieldContainer[_cloud_resource_provider_pb2.CloudResourceProvider]
    def __init__(self, owner: _Optional[_Union[_io_pb2.CloudResourceOwner, _Mapping]] = ..., search_kind: _Optional[str] = ..., providers: _Optional[_Iterable[_Union[_cloud_resource_provider_pb2.CloudResourceProvider, str]]] = ...) -> None: ...
