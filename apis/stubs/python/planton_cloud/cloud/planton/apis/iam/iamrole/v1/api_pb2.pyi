from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IamRole(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.ApiResourceMetadata
    spec: IamRoleSpec
    status: _status_pb2.ApiResourceAuditStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[IamRoleSpec, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.ApiResourceAuditStatus, _Mapping]] = ...) -> None: ...

class IamRoleSpec(_message.Message):
    __slots__ = ("role_code", "principal_type", "resource_kind", "description")
    ROLE_CODE_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    role_code: str
    principal_type: str
    resource_kind: str
    description: str
    def __init__(self, role_code: _Optional[str] = ..., principal_type: _Optional[str] = ..., resource_kind: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
