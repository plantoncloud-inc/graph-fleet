from project.planton.shared.gcp import gcp_pb2 as _gcp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpArtifactRegistryRepoStackOutputs(_message.Message):
    __slots__ = ("reader_service_account", "writer_service_account", "repo_name", "hostname", "repo_url")
    READER_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    WRITER_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    REPO_NAME_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    REPO_URL_FIELD_NUMBER: _ClassVar[int]
    reader_service_account: _gcp_pb2.GoogleServiceAccount
    writer_service_account: _gcp_pb2.GoogleServiceAccount
    repo_name: str
    hostname: str
    repo_url: str
    def __init__(self, reader_service_account: _Optional[_Union[_gcp_pb2.GoogleServiceAccount, _Mapping]] = ..., writer_service_account: _Optional[_Union[_gcp_pb2.GoogleServiceAccount, _Mapping]] = ..., repo_name: _Optional[str] = ..., hostname: _Optional[str] = ..., repo_url: _Optional[str] = ...) -> None: ...
