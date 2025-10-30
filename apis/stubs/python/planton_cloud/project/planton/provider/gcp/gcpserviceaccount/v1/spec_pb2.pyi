from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GcpServiceAccountSpec(_message.Message):
    __slots__ = ("service_account_id", "project_id", "org_id", "create_key", "project_iam_roles", "org_iam_roles")
    SERVICE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_KEY_FIELD_NUMBER: _ClassVar[int]
    PROJECT_IAM_ROLES_FIELD_NUMBER: _ClassVar[int]
    ORG_IAM_ROLES_FIELD_NUMBER: _ClassVar[int]
    service_account_id: str
    project_id: str
    org_id: str
    create_key: bool
    project_iam_roles: _containers.RepeatedScalarFieldContainer[str]
    org_iam_roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, service_account_id: _Optional[str] = ..., project_id: _Optional[str] = ..., org_id: _Optional[str] = ..., create_key: bool = ..., project_iam_roles: _Optional[_Iterable[str]] = ..., org_iam_roles: _Optional[_Iterable[str]] = ...) -> None: ...
