from cloud.planton.apis.integration.vcs import git_commit_pb2 as _git_commit_pb2
from cloud.planton.apis.servicehub.pipeline.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.servicehub.service.v1 import api_pb2 as _api_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineCreationWorkflowInput(_message.Message):
    __slots__ = ("service", "git_commit")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    service: _api_pb2_1.Service
    git_commit: _git_commit_pb2.GitCommit
    def __init__(self, service: _Optional[_Union[_api_pb2_1.Service, _Mapping]] = ..., git_commit: _Optional[_Union[_git_commit_pb2.GitCommit, _Mapping]] = ...) -> None: ...

class PipelineBuildStageWorkflowInput(_message.Message):
    __slots__ = ("service", "pipeline")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    service: _api_pb2_1.Service
    pipeline: _api_pb2.Pipeline
    def __init__(self, service: _Optional[_Union[_api_pb2_1.Service, _Mapping]] = ..., pipeline: _Optional[_Union[_api_pb2.Pipeline, _Mapping]] = ...) -> None: ...

class PipelineDeployStageWorkflowInput(_message.Message):
    __slots__ = ("service", "pipeline")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    service: _api_pb2_1.Service
    pipeline: _api_pb2.Pipeline
    def __init__(self, service: _Optional[_Union[_api_pb2_1.Service, _Mapping]] = ..., pipeline: _Optional[_Union[_api_pb2.Pipeline, _Mapping]] = ...) -> None: ...
