from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.iac.terraform import terraform_pb2 as _terraform_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TerraformBackend(_message.Message):
    __slots__ = ("type", "s3", "gcs", "azurerm")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    GCS_FIELD_NUMBER: _ClassVar[int]
    AZURERM_FIELD_NUMBER: _ClassVar[int]
    type: _terraform_pb2.TerraformBackendType
    s3: TerraformS3Backend
    gcs: TerraformGcsBackend
    azurerm: TerraformAzurermBackend
    def __init__(self, type: _Optional[_Union[_terraform_pb2.TerraformBackendType, str]] = ..., s3: _Optional[_Union[TerraformS3Backend, _Mapping]] = ..., gcs: _Optional[_Union[TerraformGcsBackend, _Mapping]] = ..., azurerm: _Optional[_Union[TerraformAzurermBackend, _Mapping]] = ...) -> None: ...

class TerraformS3Backend(_message.Message):
    __slots__ = ("bucket", "aws_access_key_id", "aws_secret_access_key", "region", "dynamodb_table")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    AWS_ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    DYNAMODB_TABLE_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str
    dynamodb_table: str
    def __init__(self, bucket: _Optional[str] = ..., aws_access_key_id: _Optional[str] = ..., aws_secret_access_key: _Optional[str] = ..., region: _Optional[str] = ..., dynamodb_table: _Optional[str] = ...) -> None: ...

class TerraformGcsBackend(_message.Message):
    __slots__ = ("gcs_bucket", "service_account_key_base64")
    GCS_BUCKET_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    gcs_bucket: str
    service_account_key_base64: str
    def __init__(self, gcs_bucket: _Optional[str] = ..., service_account_key_base64: _Optional[str] = ...) -> None: ...

class TerraformAzurermBackend(_message.Message):
    __slots__ = ("resource_group_name", "storage_account_name", "container_name", "client_id", "client_secret", "tenant_id", "subscription_id")
    RESOURCE_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    STORAGE_ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    resource_group_name: str
    storage_account_name: str
    container_name: str
    client_id: str
    client_secret: str
    tenant_id: str
    subscription_id: str
    def __init__(self, resource_group_name: _Optional[str] = ..., storage_account_name: _Optional[str] = ..., container_name: _Optional[str] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., tenant_id: _Optional[str] = ..., subscription_id: _Optional[str] = ...) -> None: ...
