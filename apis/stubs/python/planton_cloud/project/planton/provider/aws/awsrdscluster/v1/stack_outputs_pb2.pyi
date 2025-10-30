from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsRdsClusterStackOutputs(_message.Message):
    __slots__ = ("rds_cluster_endpoint", "rds_cluster_reader_endpoint", "rds_cluster_id", "rds_cluster_arn", "rds_cluster_engine", "rds_cluster_engine_version", "rds_cluster_port", "rds_subnet_group", "rds_security_group", "rds_cluster_parameter_group")
    RDS_CLUSTER_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    RDS_CLUSTER_READER_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    RDS_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    RDS_CLUSTER_ARN_FIELD_NUMBER: _ClassVar[int]
    RDS_CLUSTER_ENGINE_FIELD_NUMBER: _ClassVar[int]
    RDS_CLUSTER_ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    RDS_CLUSTER_PORT_FIELD_NUMBER: _ClassVar[int]
    RDS_SUBNET_GROUP_FIELD_NUMBER: _ClassVar[int]
    RDS_SECURITY_GROUP_FIELD_NUMBER: _ClassVar[int]
    RDS_CLUSTER_PARAMETER_GROUP_FIELD_NUMBER: _ClassVar[int]
    rds_cluster_endpoint: str
    rds_cluster_reader_endpoint: str
    rds_cluster_id: str
    rds_cluster_arn: str
    rds_cluster_engine: str
    rds_cluster_engine_version: str
    rds_cluster_port: int
    rds_subnet_group: str
    rds_security_group: str
    rds_cluster_parameter_group: str
    def __init__(self, rds_cluster_endpoint: _Optional[str] = ..., rds_cluster_reader_endpoint: _Optional[str] = ..., rds_cluster_id: _Optional[str] = ..., rds_cluster_arn: _Optional[str] = ..., rds_cluster_engine: _Optional[str] = ..., rds_cluster_engine_version: _Optional[str] = ..., rds_cluster_port: _Optional[int] = ..., rds_subnet_group: _Optional[str] = ..., rds_security_group: _Optional[str] = ..., rds_cluster_parameter_group: _Optional[str] = ...) -> None: ...
