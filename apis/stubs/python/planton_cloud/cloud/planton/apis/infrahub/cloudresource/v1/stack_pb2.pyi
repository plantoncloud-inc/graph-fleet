from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.infrahub.cloudresource.v1 import cloud_object_pb2 as _cloud_object_pb2
from cloud.planton.apis.infrahub.iacmodule.v1 import pulumi_pb2 as _pulumi_pb2
from cloud.planton.apis.infrahub.iacmodule.v1 import terraform_pb2 as _terraform_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from project.planton.shared import iac_pb2 as _iac_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceStackExecuteInput(_message.Message):
    __slots__ = ("stack_job_id", "provisioner", "pulumi", "terraform", "kind", "metadata", "cloud_object_stack_input")
    STACK_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    PROVISIONER_FIELD_NUMBER: _ClassVar[int]
    PULUMI_FIELD_NUMBER: _ClassVar[int]
    TERRAFORM_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CLOUD_OBJECT_STACK_INPUT_FIELD_NUMBER: _ClassVar[int]
    stack_job_id: str
    provisioner: _iac_pb2.IacProvisioner
    pulumi: _pulumi_pb2.PulumiStackInfo
    terraform: _terraform_pb2.TerraformStackInfo
    kind: _cloud_resource_kind_pb2.CloudResourceKind
    metadata: _metadata_pb2.ApiResourceMetadata
    cloud_object_stack_input: _cloud_object_pb2.CloudObjectStackInput
    def __init__(self, stack_job_id: _Optional[str] = ..., provisioner: _Optional[_Union[_iac_pb2.IacProvisioner, str]] = ..., pulumi: _Optional[_Union[_pulumi_pb2.PulumiStackInfo, _Mapping]] = ..., terraform: _Optional[_Union[_terraform_pb2.TerraformStackInfo, _Mapping]] = ..., kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., cloud_object_stack_input: _Optional[_Union[_cloud_object_pb2.CloudObjectStackInput, _Mapping]] = ...) -> None: ...
