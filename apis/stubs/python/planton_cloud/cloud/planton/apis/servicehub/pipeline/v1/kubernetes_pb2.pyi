from cloud.planton.apis.connect.dockercredential.v1 import spec_pb2 as _spec_pb2
from cloud.planton.apis.servicehub.service.v1 import api_pb2 as _api_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineKubernetesInput(_message.Message):
    __slots__ = ("service", "pipeline_id", "pipeline_build_stage_workflow_id", "container_image", "git_revision", "git_auth_secret_name")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_BUILD_STAGE_WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    GIT_REVISION_FIELD_NUMBER: _ClassVar[int]
    GIT_AUTH_SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    service: _api_pb2.Service
    pipeline_id: str
    pipeline_build_stage_workflow_id: str
    container_image: PipelineKubernetesInputContainerImage
    git_revision: str
    git_auth_secret_name: str
    def __init__(self, service: _Optional[_Union[_api_pb2.Service, _Mapping]] = ..., pipeline_id: _Optional[str] = ..., pipeline_build_stage_workflow_id: _Optional[str] = ..., container_image: _Optional[_Union[PipelineKubernetesInputContainerImage, _Mapping]] = ..., git_revision: _Optional[str] = ..., git_auth_secret_name: _Optional[str] = ...) -> None: ...

class PipelineKubernetesInputContainerImage(_message.Message):
    __slots__ = ("container_image_name", "docker_push_credential")
    CONTAINER_IMAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    DOCKER_PUSH_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    container_image_name: str
    docker_push_credential: _spec_pb2.DockerCredentialSpec
    def __init__(self, container_image_name: _Optional[str] = ..., docker_push_credential: _Optional[_Union[_spec_pb2.DockerCredentialSpec, _Mapping]] = ...) -> None: ...
