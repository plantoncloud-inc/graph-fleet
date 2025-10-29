from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from cloud.planton.apis.commons.apiresource import metadata_pb2 as _metadata_pb2
from cloud.planton.apis.commons.apiresource import status_pb2 as _status_pb2
from project.planton.shared.kubernetes import kubernetes_pb2 as _kubernetes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageLevelProtoValidateConditionalTest(_message.Message):
    __slots__ = ("cloud_provider", "gcp_spec", "aws_spec")
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    GCP_SPEC_FIELD_NUMBER: _ClassVar[int]
    AWS_SPEC_FIELD_NUMBER: _ClassVar[int]
    cloud_provider: int
    gcp_spec: GcpSpecTest
    aws_spec: AwsSpecTest
    def __init__(self, cloud_provider: _Optional[int] = ..., gcp_spec: _Optional[_Union[GcpSpecTest, _Mapping]] = ..., aws_spec: _Optional[_Union[AwsSpecTest, _Mapping]] = ...) -> None: ...

class GcpSpecTest(_message.Message):
    __slots__ = ("project_id", "no_validation_field")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NO_VALIDATION_FIELD_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    no_validation_field: str
    def __init__(self, project_id: _Optional[str] = ..., no_validation_field: _Optional[str] = ...) -> None: ...

class AwsSpecTest(_message.Message):
    __slots__ = ("account_id", "no_validation_field")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NO_VALIDATION_FIELD_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    no_validation_field: str
    def __init__(self, account_id: _Optional[str] = ..., no_validation_field: _Optional[str] = ...) -> None: ...

class ApiResourceKubernetesTest(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.ApiResourceMetadata
    spec: ApiResourceKubernetesTestSpec
    status: ApiResourceKubernetesTestStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.ApiResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[ApiResourceKubernetesTestSpec, _Mapping]] = ..., status: _Optional[_Union[ApiResourceKubernetesTestStatus, _Mapping]] = ...) -> None: ...

class ApiResourceKubernetesTestSpec(_message.Message):
    __slots__ = ("container", "ingress")
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    container: ApiResourceKubernetesSpecContainerSpec
    ingress: _kubernetes_pb2.IngressSpec
    def __init__(self, container: _Optional[_Union[ApiResourceKubernetesSpecContainerSpec, _Mapping]] = ..., ingress: _Optional[_Union[_kubernetes_pb2.IngressSpec, _Mapping]] = ...) -> None: ...

class ApiResourceKubernetesTestStatus(_message.Message):
    __slots__ = ("audit", "stack_job_id", "namespace", "service", "port_forward_command", "kube_endpoint", "external_cluster_hostname", "internal_cluster_hostname")
    AUDIT_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    PORT_FORWARD_COMMAND_FIELD_NUMBER: _ClassVar[int]
    KUBE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CLUSTER_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_CLUSTER_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    audit: _status_pb2.ApiResourceAudit
    stack_job_id: str
    namespace: str
    service: str
    port_forward_command: str
    kube_endpoint: str
    external_cluster_hostname: str
    internal_cluster_hostname: str
    def __init__(self, audit: _Optional[_Union[_status_pb2.ApiResourceAudit, _Mapping]] = ..., stack_job_id: _Optional[str] = ..., namespace: _Optional[str] = ..., service: _Optional[str] = ..., port_forward_command: _Optional[str] = ..., kube_endpoint: _Optional[str] = ..., external_cluster_hostname: _Optional[str] = ..., internal_cluster_hostname: _Optional[str] = ...) -> None: ...

class ApiResourceKubernetesSpecContainerSpec(_message.Message):
    __slots__ = ("replicas", "resources", "disk_size")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    resources: _kubernetes_pb2.ContainerResources
    disk_size: str
    def __init__(self, replicas: _Optional[int] = ..., resources: _Optional[_Union[_kubernetes_pb2.ContainerResources, _Mapping]] = ..., disk_size: _Optional[str] = ...) -> None: ...
