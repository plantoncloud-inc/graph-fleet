from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEcsClusterStackOutputs(_message.Message):
    __slots__ = ("cluster_name", "cluster_arn", "cluster_capacity_providers")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ARN_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CAPACITY_PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    cluster_arn: str
    cluster_capacity_providers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cluster_name: _Optional[str] = ..., cluster_arn: _Optional[str] = ..., cluster_capacity_providers: _Optional[_Iterable[str]] = ...) -> None: ...
