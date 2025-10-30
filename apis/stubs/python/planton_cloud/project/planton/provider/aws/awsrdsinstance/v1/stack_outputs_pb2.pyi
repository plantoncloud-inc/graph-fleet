from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsRdsInstanceStackOutputs(_message.Message):
    __slots__ = ("rds_instance_id", "rds_instance_arn", "rds_instance_endpoint", "rds_instance_port", "rds_subnet_group", "rds_security_group", "rds_parameter_group")
    RDS_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    RDS_INSTANCE_ARN_FIELD_NUMBER: _ClassVar[int]
    RDS_INSTANCE_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    RDS_INSTANCE_PORT_FIELD_NUMBER: _ClassVar[int]
    RDS_SUBNET_GROUP_FIELD_NUMBER: _ClassVar[int]
    RDS_SECURITY_GROUP_FIELD_NUMBER: _ClassVar[int]
    RDS_PARAMETER_GROUP_FIELD_NUMBER: _ClassVar[int]
    rds_instance_id: str
    rds_instance_arn: str
    rds_instance_endpoint: str
    rds_instance_port: int
    rds_subnet_group: str
    rds_security_group: str
    rds_parameter_group: str
    def __init__(self, rds_instance_id: _Optional[str] = ..., rds_instance_arn: _Optional[str] = ..., rds_instance_endpoint: _Optional[str] = ..., rds_instance_port: _Optional[int] = ..., rds_subnet_group: _Optional[str] = ..., rds_security_group: _Optional[str] = ..., rds_parameter_group: _Optional[str] = ...) -> None: ...
