from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpRouterNatSpec(_message.Message):
    __slots__ = ("vpc_self_link", "region", "subnetwork_self_links", "nat_ip_names")
    VPC_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SUBNETWORK_SELF_LINKS_FIELD_NUMBER: _ClassVar[int]
    NAT_IP_NAMES_FIELD_NUMBER: _ClassVar[int]
    vpc_self_link: _foreign_key_pb2.StringValueOrRef
    region: str
    subnetwork_self_links: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    nat_ip_names: _containers.RepeatedCompositeFieldContainer[_foreign_key_pb2.StringValueOrRef]
    def __init__(self, vpc_self_link: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., region: _Optional[str] = ..., subnetwork_self_links: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ..., nat_ip_names: _Optional[_Iterable[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]]] = ...) -> None: ...
