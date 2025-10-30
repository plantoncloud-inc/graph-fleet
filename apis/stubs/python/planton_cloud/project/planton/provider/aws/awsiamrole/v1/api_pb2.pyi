from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.aws.awsiamrole.v1 import spec_pb2 as _spec_pb2
from project.planton.provider.aws.awsiamrole.v1 import stack_outputs_pb2 as _stack_outputs_pb2
from project.planton.shared import metadata_pb2 as _metadata_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsIamRole(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: _metadata_pb2.CloudResourceMetadata
    spec: _spec_pb2.AwsIamRoleSpec
    status: AwsIamRoleStatus
    def __init__(self, api_version: _Optional[str] = ..., kind: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.CloudResourceMetadata, _Mapping]] = ..., spec: _Optional[_Union[_spec_pb2.AwsIamRoleSpec, _Mapping]] = ..., status: _Optional[_Union[AwsIamRoleStatus, _Mapping]] = ...) -> None: ...

class AwsIamRoleStatus(_message.Message):
    __slots__ = ("outputs",)
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    outputs: _stack_outputs_pb2.AwsIamRoleStackOutputs
    def __init__(self, outputs: _Optional[_Union[_stack_outputs_pb2.AwsIamRoleStackOutputs, _Mapping]] = ...) -> None: ...
