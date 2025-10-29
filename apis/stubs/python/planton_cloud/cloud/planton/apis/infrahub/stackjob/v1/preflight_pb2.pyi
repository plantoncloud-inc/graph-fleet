from cloud.planton.apis.commons.apiresource import io_pb2 as _io_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from project.planton.shared.cloudresourcekind import cloud_resource_kind_pb2 as _cloud_resource_kind_pb2
from project.planton.shared import iac_pb2 as _iac_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckStackJobEssentialsInput(_message.Message):
    __slots__ = ("cloud_resource_kind", "cloud_resource_owner")
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_OWNER_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    cloud_resource_owner: _io_pb2.CloudResourceOwner
    def __init__(self, cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ..., cloud_resource_owner: _Optional[_Union[_io_pb2.CloudResourceOwner, _Mapping]] = ...) -> None: ...

class CheckStackJobEssentialsResponse(_message.Message):
    __slots__ = ("stack_job_runner", "iac_module", "backend_credential", "flow_control", "provider_credential")
    STACK_JOB_RUNNER_FIELD_NUMBER: _ClassVar[int]
    IAC_MODULE_FIELD_NUMBER: _ClassVar[int]
    BACKEND_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    FLOW_CONTROL_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    stack_job_runner: StackJobRunnerPreflightCheck
    iac_module: IacModulePreflightCheck
    backend_credential: BackendCredentialPreflightCheck
    flow_control: FlowControlPolicyPreflightCheck
    provider_credential: ProviderCredentialPreflightCheck
    def __init__(self, stack_job_runner: _Optional[_Union[StackJobRunnerPreflightCheck, _Mapping]] = ..., iac_module: _Optional[_Union[IacModulePreflightCheck, _Mapping]] = ..., backend_credential: _Optional[_Union[BackendCredentialPreflightCheck, _Mapping]] = ..., flow_control: _Optional[_Union[FlowControlPolicyPreflightCheck, _Mapping]] = ..., provider_credential: _Optional[_Union[ProviderCredentialPreflightCheck, _Mapping]] = ...) -> None: ...

class StackJobRunnerPreflightCheck(_message.Message):
    __slots__ = ("passed", "errors", "stack_job_runner_info")
    PASSED_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_RUNNER_INFO_FIELD_NUMBER: _ClassVar[int]
    passed: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    stack_job_runner_info: _io_pb2.ApiResourceKindAndNameAndId
    def __init__(self, passed: bool = ..., errors: _Optional[_Iterable[str]] = ..., stack_job_runner_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ...) -> None: ...

class IacModulePreflightCheck(_message.Message):
    __slots__ = ("passed", "errors", "iac_module_info", "provisioner")
    PASSED_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    IAC_MODULE_INFO_FIELD_NUMBER: _ClassVar[int]
    PROVISIONER_FIELD_NUMBER: _ClassVar[int]
    passed: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    iac_module_info: _io_pb2.ApiResourceKindAndNameAndId
    provisioner: _iac_pb2.IacProvisioner
    def __init__(self, passed: bool = ..., errors: _Optional[_Iterable[str]] = ..., iac_module_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ..., provisioner: _Optional[_Union[_iac_pb2.IacProvisioner, str]] = ...) -> None: ...

class BackendCredentialPreflightCheck(_message.Message):
    __slots__ = ("passed", "errors", "backend_credential_info")
    PASSED_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    BACKEND_CREDENTIAL_INFO_FIELD_NUMBER: _ClassVar[int]
    passed: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    backend_credential_info: _io_pb2.ApiResourceKindAndNameAndId
    def __init__(self, passed: bool = ..., errors: _Optional[_Iterable[str]] = ..., backend_credential_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ...) -> None: ...

class FlowControlPolicyPreflightCheck(_message.Message):
    __slots__ = ("passed", "errors", "flow_control_policy_info")
    PASSED_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    FLOW_CONTROL_POLICY_INFO_FIELD_NUMBER: _ClassVar[int]
    passed: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    flow_control_policy_info: _io_pb2.ApiResourceKindAndNameAndId
    def __init__(self, passed: bool = ..., errors: _Optional[_Iterable[str]] = ..., flow_control_policy_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ...) -> None: ...

class ProviderCredentialPreflightCheck(_message.Message):
    __slots__ = ("passed", "errors", "provider_credential_info", "info")
    PASSED_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CREDENTIAL_INFO_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    passed: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    provider_credential_info: _io_pb2.ApiResourceKindAndNameAndId
    info: str
    def __init__(self, passed: bool = ..., errors: _Optional[_Iterable[str]] = ..., provider_credential_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ..., info: _Optional[str] = ...) -> None: ...

class WhichStackJobEssentialResponse(_message.Message):
    __slots__ = ("visited_selectors", "found", "errors", "result_info")
    VISITED_SELECTORS_FIELD_NUMBER: _ClassVar[int]
    FOUND_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    RESULT_INFO_FIELD_NUMBER: _ClassVar[int]
    visited_selectors: _containers.RepeatedCompositeFieldContainer[_selector_pb2.ApiResourceSelector]
    found: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    result_info: _io_pb2.ApiResourceKindAndNameAndId
    def __init__(self, visited_selectors: _Optional[_Iterable[_Union[_selector_pb2.ApiResourceSelector, _Mapping]]] = ..., found: bool = ..., errors: _Optional[_Iterable[str]] = ..., result_info: _Optional[_Union[_io_pb2.ApiResourceKindAndNameAndId, _Mapping]] = ...) -> None: ...

class WhichIacModuleInput(_message.Message):
    __slots__ = ("org", "cloud_resource_kind")
    ORG_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    org: str
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    def __init__(self, org: _Optional[str] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ...) -> None: ...

class WhichBackendCredentialInput(_message.Message):
    __slots__ = ("org", "cloud_resource_kind")
    ORG_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    org: str
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    def __init__(self, org: _Optional[str] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ...) -> None: ...

class WhichFlowControlPolicyInput(_message.Message):
    __slots__ = ("selector", "cloud_resource_owner")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_OWNER_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    cloud_resource_owner: _io_pb2.CloudResourceOwner
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., cloud_resource_owner: _Optional[_Union[_io_pb2.CloudResourceOwner, _Mapping]] = ...) -> None: ...

class WhichProviderCredentialInput(_message.Message):
    __slots__ = ("cloud_resource_owner", "cloud_resource_kind")
    CLOUD_RESOURCE_OWNER_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    cloud_resource_owner: _io_pb2.CloudResourceOwner
    cloud_resource_kind: _cloud_resource_kind_pb2.CloudResourceKind
    def __init__(self, cloud_resource_owner: _Optional[_Union[_io_pb2.CloudResourceOwner, _Mapping]] = ..., cloud_resource_kind: _Optional[_Union[_cloud_resource_kind_pb2.CloudResourceKind, str]] = ...) -> None: ...
