from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEcsServiceStackOutputs(_message.Message):
    __slots__ = ("aws_ecs_service_name", "ecs_cluster_name", "load_balancer_dns_name", "service_url", "service_discovery_name", "cloudwatch_log_group_name", "cloudwatch_log_group_arn", "service_arn", "target_group_arn")
    AWS_ECS_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ECS_CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_URL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_DISCOVERY_NAME_FIELD_NUMBER: _ClassVar[int]
    CLOUDWATCH_LOG_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    CLOUDWATCH_LOG_GROUP_ARN_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ARN_FIELD_NUMBER: _ClassVar[int]
    TARGET_GROUP_ARN_FIELD_NUMBER: _ClassVar[int]
    aws_ecs_service_name: str
    ecs_cluster_name: str
    load_balancer_dns_name: str
    service_url: str
    service_discovery_name: str
    cloudwatch_log_group_name: str
    cloudwatch_log_group_arn: str
    service_arn: str
    target_group_arn: str
    def __init__(self, aws_ecs_service_name: _Optional[str] = ..., ecs_cluster_name: _Optional[str] = ..., load_balancer_dns_name: _Optional[str] = ..., service_url: _Optional[str] = ..., service_discovery_name: _Optional[str] = ..., cloudwatch_log_group_name: _Optional[str] = ..., cloudwatch_log_group_arn: _Optional[str] = ..., service_arn: _Optional[str] = ..., target_group_arn: _Optional[str] = ...) -> None: ...
