from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CivoVpcSpec(_message.Message):
    __slots__ = ("civo_credential_id", "network_name", "region", "ip_range_cidr", "is_default_for_region", "description")
    CIVO_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    NETWORK_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    IP_RANGE_CIDR_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FOR_REGION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    civo_credential_id: str
    network_name: str
    region: str
    ip_range_cidr: str
    is_default_for_region: bool
    description: str
    def __init__(self, civo_credential_id: _Optional[str] = ..., network_name: _Optional[str] = ..., region: _Optional[str] = ..., ip_range_cidr: _Optional[str] = ..., is_default_for_region: bool = ..., description: _Optional[str] = ...) -> None: ...
