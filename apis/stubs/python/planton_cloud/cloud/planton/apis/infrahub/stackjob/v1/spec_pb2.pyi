from cloud.planton.apis.commons.apiresource import io_pb2 as _io_pb2
from cloud.planton.apis.infrahub.cloudresource.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.infrahub.cloudresource.v1 import mutator_pb2 as _mutator_pb2
from cloud.planton.apis.infrahub.stackjob.v1 import enum_pb2 as _enum_pb2
from project.planton.shared import iac_pb2 as _iac_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StackJobSpec(_message.Message):
    __slots__ = ("stack_job_operation", "essentials", "cloud_resource", "cloud_resource_mutator")
    STACK_JOB_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ESSENTIALS_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_MUTATOR_FIELD_NUMBER: _ClassVar[int]
    stack_job_operation: _enum_pb2.StackJobOperationType
    essentials: StackJobEssentials
    cloud_resource: _api_pb2.CloudResource
    cloud_resource_mutator: _mutator_pb2.CloudResourceMutator
    def __init__(self, stack_job_operation: _Optional[_Union[_enum_pb2.StackJobOperationType, str]] = ..., essentials: _Optional[_Union[StackJobEssentials, _Mapping]] = ..., cloud_resource: _Optional[_Union[_api_pb2.CloudResource, _Mapping]] = ..., cloud_resource_mutator: _Optional[_Union[_mutator_pb2.CloudResourceMutator, _Mapping]] = ...) -> None: ...

class StackJobEssentials(_message.Message):
    __slots__ = ("stack_job_runner_info", "iac_module_info", "provisioner", "backend_credential_info", "flow_control_policy_info", "provider_credential_info")
    STACK_JOB_RUNNER_INFO_FIELD_NUMBER: _ClassVar[int]
    IAC_MODULE_INFO_FIELD_NUMBER: _ClassVar[int]
    PROVISIONER_FIELD_NUMBER: _ClassVar[int]
    BACKEND_CREDENTIAL_INFO_FIELD_NUMBER: _ClassVar[int]
    FLOW_CONTROL_POLICY_INFO_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CREDENTIAL_INFO_FIELD_NUMBER: _ClassVar[int]
    stack_job_runner_info: _io_pb2.ApiResourceKindAndNameAndId
    iac_module_info: _io_pb2.ApiResourceKindAndNameAndId
    provisioner: _iac_pb2.IacProvisioner
    backend_credential_info: _io_pb2.ApiResourceKindAndNameAndId
    flow_control_policy_info: _io_pb2.ApiResourceKindAndNameAndId
    provider_credential_info: _io_pb2.ApiResourceKindAndNameAndId
    def __init__(self, stack_job_runner_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ..., iac_module_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ..., provisioner: _Optional[_Union[_iac_pb2.IacProvisioner, str]] = ..., backend_credential_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ..., flow_control_policy_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ..., provider_credential_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ...) -> None: ...
