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

class AwsEksNodeGroupCapacityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    on_demand: _ClassVar[AwsEksNodeGroupCapacityType]
    spot: _ClassVar[AwsEksNodeGroupCapacityType]
on_demand: AwsEksNodeGroupCapacityType
spot: AwsEksNodeGroupCapacityType

class AwsEksNodeGroupSpec(_message.Message):
    __slots__ = ("cluster_name", "node_role_arn", "subnet_ids", "instance_type", "scaling", "capacity_type", "disk_size_gb", "ssh_key_name", "labels")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    SUBNET_IDS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCALING_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_GB_FIELD_NUMBER: _ClassVar[int]
    SSH_KEY_NAME_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    cluster_name: _foreign_key_pb2.StringValueOrRef
    node_role_arn: _foreign_key_pb2.StringValueOrRef
    subnet_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    instance_type: str
    scaling: AwsEksNodeGroupScalingConfig
    capacity_type: AwsEksNodeGroupCapacityType
    disk_size_gb: int
    ssh_key_name: str
    labels: _containers.ScalarMap[str, str]
    def __init__(self, cluster_name: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., node_role_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., subnet_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., instance_type: _Optional[str] = ..., scaling: _Optional[_Union[AwsEksNodeGroupScalingConfig, _Mapping]] = ..., capacity_type: _Optional[_Union[AwsEksNodeGroupCapacityType, str]] = ..., disk_size_gb: _Optional[int] = ..., ssh_key_name: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ...) -> None: ...

class AwsEksNodeGroupScalingConfig(_message.Message):
    __slots__ = ("min_size", "max_size", "desired_size")
    MIN_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_SIZE_FIELD_NUMBER: _ClassVar[int]
    DESIRED_SIZE_FIELD_NUMBER: _ClassVar[int]
    min_size: int
    max_size: int
    desired_size: int
    def __init__(self, min_size: _Optional[int] = ..., max_size: _Optional[int] = ..., desired_size: _Optional[int] = ...) -> None: ...
