from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEksNodeGroupStackOutputs(_message.Message):
    __slots__ = ("nodegroup_name", "asg_name", "remote_access_sg_id", "instance_profile_arn")
    NODEGROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    ASG_NAME_FIELD_NUMBER: _ClassVar[int]
    REMOTE_ACCESS_SG_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_PROFILE_ARN_FIELD_NUMBER: _ClassVar[int]
    nodegroup_name: str
    asg_name: str
    remote_access_sg_id: str
    instance_profile_arn: str
    def __init__(self, nodegroup_name: _Optional[str] = ..., asg_name: _Optional[str] = ..., remote_access_sg_id: _Optional[str] = ..., instance_profile_arn: _Optional[str] = ...) -> None: ...
