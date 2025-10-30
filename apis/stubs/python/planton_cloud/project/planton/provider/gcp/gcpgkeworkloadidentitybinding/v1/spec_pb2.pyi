from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGkeWorkloadIdentityBindingSpec(_message.Message):
    __slots__ = ("project_id", "service_account_email", "ksa_namespace", "ksa_name")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    KSA_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    KSA_NAME_FIELD_NUMBER: _ClassVar[int]
    project_id: _foreign_key_pb2.StringValueOrRef
    service_account_email: _foreign_key_pb2.StringValueOrRef
    ksa_namespace: str
    ksa_name: str
    def __init__(self, project_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., service_account_email: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., ksa_namespace: _Optional[str] = ..., ksa_name: _Optional[str] = ...) -> None: ...
