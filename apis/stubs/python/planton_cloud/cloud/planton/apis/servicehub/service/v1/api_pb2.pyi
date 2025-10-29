from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from cloud.planton.apis.servicehub.service.v1 import spec_pb2 as _spec_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Service(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.ApiResourceMetadata
    spec: _spec_pb2.ServiceSpec
    status: ServiceStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[_spec_pb2.ServiceSpec, _Mapping]] = ..., status: _Optional[_Union[ServiceStatus, _Mapping]] = ...) -> None: ...

class ServiceStatus(_message.Message):
    __slots__ = ("audit", "env_deployment_map")
    class EnvDeploymentMapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ServiceDeployment
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ServiceDeployment, _Mapping]] = ...) -> None: ...
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    ENV_DEPLOYMENT_MAP_FIELD_NUMBER: _ClassVar[int]
    audit: _status_pb2.ApiResourceAudit
    env_deployment_map: _containers.MessageMap[str, ServiceDeployment]
    def __init__(self, audit: _Optional[_Union[_status_pb2.ApiResourceAudit, _Mapping]] = ..., env_deployment_map: _Optional[_Mapping[str, ServiceDeployment]] = ...) -> None: ...

class ServiceDeployment(_message.Message):
    __slots__ = ("resource_kind", "resource_id")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    resource_kind: _api_resource_kind_pb2.ApiResourceKind
    resource_id: str
    def __init__(self, resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., resource_id: _Optional[str] = ...) -> None: ...
