from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.civo import region_pb2 as _region_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CivoComputeInstanceSpec(_message.Message):
    __slots__ = ("instance_name", "region", "size", "image", "network", "ssh_key_ids", "firewall_ids", "volume_ids", "reserved_ip_id", "tags", "user_data")
    INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    SSH_KEY_IDS_FIELD_NUMBER: _ClassVar[int]
    FIREWALL_IDS_FIELD_NUMBER: _ClassVar[int]
    VOLUME_IDS_FIELD_NUMBER: _ClassVar[int]
    RESERVED_IP_ID_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    instance_name: str
    region: _region_pb2.CivoRegion
    size: str
    image: str
    network: _foreign_key_pb2.StringValueOrRef
    ssh_key_ids: _containers.RepeatedScalarFieldContainer[str]
    firewall_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    volume_ids: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    reserved_ip_id: _foreign_key_pb2.StringValueOrRef
    tags: _containers.RepeatedScalarFieldContainer[str]
    user_data: str
    def __init__(self, instance_name: _Optional[str] = ..., region: _Optional[_Union[_region_pb2.CivoRegion, str]] = ..., size: _Optional[str] = ..., image: _Optional[str] = ..., network: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., ssh_key_ids: _Optional[_Iterable[str]] = ..., firewall_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., volume_ids: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., reserved_ip_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., tags: _Optional[_Iterable[str]] = ..., user_data: _Optional[str] = ...) -> None: ...
