from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEc2InstanceConnectionMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SSM: _ClassVar[AwsEc2InstanceConnectionMethod]
    BASTION: _ClassVar[AwsEc2InstanceConnectionMethod]
    INSTANCE_CONNECT: _ClassVar[AwsEc2InstanceConnectionMethod]
SSM: AwsEc2InstanceConnectionMethod
BASTION: AwsEc2InstanceConnectionMethod
INSTANCE_CONNECT: AwsEc2InstanceConnectionMethod

class AwsEc2InstanceSpec(_message.Message):
    __slots__ = ("instance_name", "ami_id", "instance_type", "subnet_id", "security_group_ids", "connection_method", "iam_instance_profile_arn", "key_name", "root_volume_size_gb", "tags", "user_data", "ebs_optimized", "disable_api_termination")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    AMI_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUBNET_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_METHOD_FIELD_NUMBER: _ClassVar[int]
    IAM_INSTANCE_PROFILE_ARN_FIELD_NUMBER: _ClassVar[int]
    KEY_NAME_FIELD_NUMBER: _ClassVar[int]
    ROOT_VOLUME_SIZE_GB_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    EBS_OPTIMIZED_FIELD_NUMBER: _ClassVar[int]
    DISABLE_API_TERMINATION_FIELD_NUMBER: _ClassVar[int]
    instance_name: str
    ami_id: str
    instance_type: str
    subnet_id: _foreign_key_pb2.StringValueOrRef
    security_group_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    connection_method: AwsEc2InstanceConnectionMethod
    iam_instance_profile_arn: _foreign_key_pb2.StringValueOrRef
    key_name: str
    root_volume_size_gb: int
    tags: _containers.ScalarMap[str, str]
    user_data: str
    ebs_optimized: bool
    disable_api_termination: bool
    def __init__(self, instance_name: _Optional[str] = ..., ami_id: _Optional[str] = ..., instance_type: _Optional[str] = ..., subnet_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., security_group_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., connection_method: _Optional[_Union[AwsEc2InstanceConnectionMethod, str]] = ..., iam_instance_profile_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., key_name: _Optional[str] = ..., root_volume_size_gb: _Optional[int] = ..., tags: _Optional[_Mapping[str, str]] = ..., user_data: _Optional[str] = ..., ebs_optimized: bool = ..., disable_api_termination: bool = ...) -> None: ...
