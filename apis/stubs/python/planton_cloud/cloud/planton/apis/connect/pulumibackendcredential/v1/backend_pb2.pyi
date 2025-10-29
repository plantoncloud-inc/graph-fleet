from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.iac.pulumi import pulumi_pb2 as _pulumi_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PulumiBackend(_message.Message):
    __slots__ = ("type", "http", "s3", "gcs", "azurerm")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HTTP_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    GCS_FIELD_NUMBER: _ClassVar[int]
    AZURERM_FIELD_NUMBER: _ClassVar[int]
    type: _pulumi_pb2.PulumiBackendType
    http: PulumiHttpBackend
    s3: PulumiS3Backend
    gcs: PulumiGcsBackend
    azurerm: PulumiAzurermBackend
    def __init__(self, type: _Optional[_Union[_pulumi_pb2.PulumiBackendType, str]] = ..., http: _Optional[_Union[PulumiHttpBackend, _Mapping]] = ..., s3: _Optional[_Union[PulumiS3Backend, _Mapping]] = ..., gcs: _Optional[_Union[PulumiGcsBackend, _Mapping]] = ..., azurerm: _Optional[_Union[PulumiAzurermBackend, _Mapping]] = ...) -> None: ...

class PulumiHttpBackend(_message.Message):
    __slots__ = ("api_url", "pulumi_organization", "access_token")
    API_URL_FIELD_NUMBER: _ClassVar[int]
    PULUMI_ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    api_url: str
    pulumi_organization: str
    access_token: str
    def __init__(self, api_url: _Optional[str] = ..., pulumi_organization: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class PulumiS3Backend(_message.Message):
    __slots__ = ("s3_bucket", "aws_access_key_id", "aws_secret_access_key")
    S3_BUCKET_FIELD_NUMBER: _ClassVar[int]
    AWS_ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    s3_bucket: str
    aws_access_key_id: str
    aws_secret_access_key: str
    def __init__(self, s3_bucket: _Optional[str] = ..., aws_access_key_id: _Optional[str] = ..., aws_secret_access_key: _Optional[str] = ...) -> None: ...

class PulumiGcsBackend(_message.Message):
    __slots__ = ("gcs_bucket", "service_account_key_base64")
    GCS_BUCKET_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    gcs_bucket: str
    service_account_key_base64: str
    def __init__(self, gcs_bucket: _Optional[str] = ..., service_account_key_base64: _Optional[str] = ...) -> None: ...

class PulumiAzurermBackend(_message.Message):
    __slots__ = ("blob_storage_container", "storage_account_name", "storage_account_key")
    BLOB_STORAGE_CONTAINER_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ACCOUNT_KEY_FIELD_NUMBER: _ClassVar[int]
    blob_storage_container: str
    storage_account_name: str
    storage_account_key: str
    def __init__(self, blob_storage_container: _Optional[str] = ..., storage_account_name: _Optional[str] = ..., storage_account_key: _Optional[str] = ...) -> None: ...
