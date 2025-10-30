from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsCertManagerCertSpec(_message.Message):
    __slots__ = ("primary_domain_name", "alternate_domain_names", "route53_hosted_zone_id", "validation_method")
    PRIMARY_DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    ALTERNATE_DOMAIN_NAMES_FIELD_NUMBER: _ClassVar[int]
    ROUTE53_HOSTED_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    primary_domain_name: str
    alternate_domain_names: _containers.RepeatedScalarFieldContainer[str]
    route53_hosted_zone_id: _foreign_key_pb2.StringValueOrRef
    validation_method: str
    def __init__(self, primary_domain_name: _Optional[str] = ..., alternate_domain_names: _Optional[_Iterable[str]] = ..., route53_hosted_zone_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., validation_method: _Optional[str] = ...) -> None: ...
