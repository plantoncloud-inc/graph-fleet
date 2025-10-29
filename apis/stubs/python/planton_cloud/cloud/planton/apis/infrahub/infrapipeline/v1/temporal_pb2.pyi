from cloud.planton.apis.infrahub.infrapipeline.v1 import api_pb2 as _api_pb2
from cloud.planton.apis.infrahub.infraproject.v1 import api_pb2 as _api_pb2_1
from cloud.planton.apis.integration.vcs import git_commit_pb2 as _git_commit_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InfraPipelineCreationWorkflowInput(_message.Message):
    __slots__ = ("infra_project", "git_commit")
    INFRA_PROJECT_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    infra_project: _api_pb2_1.InfraProject
    git_commit: _git_commit_pb2.GitCommit
    def __init__(self, infra_project: _Optional[_Union[_api_pb2_1.InfraProject, _Mapping]] = ..., git_commit: _Optional[_Union[_git_commit_pb2.GitCommit, _Mapping]] = ...) -> None: ...

class InfraPipelineBuildStageWorkflowInput(_message.Message):
    __slots__ = ("infra_project", "infra_pipeline")
    INFRA_PROJECT_FIELD_NUMBER: _ClassVar[int]
    INFRA_PIPELINE_FIELD_NUMBER: _ClassVar[int]
    infra_project: _api_pb2_1.InfraProject
    infra_pipeline: _api_pb2.InfraPipeline
    def __init__(self, infra_project: _Optional[_Union[_api_pb2_1.InfraProject, _Mapping]] = ..., infra_pipeline: _Optional[_Union[_api_pb2.InfraPipeline, _Mapping]] = ...) -> None: ...

class InfraPipelineDeployStageWorkflowInput(_message.Message):
    __slots__ = ("infra_project", "infra_pipeline")
    INFRA_PROJECT_FIELD_NUMBER: _ClassVar[int]
    INFRA_PIPELINE_FIELD_NUMBER: _ClassVar[int]
    infra_project: _api_pb2_1.InfraProject
    infra_pipeline: _api_pb2.InfraPipeline
    def __init__(self, infra_project: _Optional[_Union[_api_pb2_1.InfraProject, _Mapping]] = ..., infra_pipeline: _Optional[_Union[_api_pb2.InfraPipeline, _Mapping]] = ...) -> None: ...
