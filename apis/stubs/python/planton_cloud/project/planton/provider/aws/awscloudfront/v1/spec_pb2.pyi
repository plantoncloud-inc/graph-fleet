from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsCloudFrontSpec(_message.Message):
    __slots__ = ("enabled", "aliases", "certificate_arn", "price_class", "origins", "default_root_object")
    class PriceClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRICE_CLASS_UNSPECIFIED: _ClassVar[AwsCloudFrontSpec.PriceClass]
        PRICE_CLASS_100: _ClassVar[AwsCloudFrontSpec.PriceClass]
        PRICE_CLASS_200: _ClassVar[AwsCloudFrontSpec.PriceClass]
        PRICE_CLASS_ALL: _ClassVar[AwsCloudFrontSpec.PriceClass]
    PRICE_CLASS_UNSPECIFIED: AwsCloudFrontSpec.PriceClass
    PRICE_CLASS_100: AwsCloudFrontSpec.PriceClass
    PRICE_CLASS_200: AwsCloudFrontSpec.PriceClass
    PRICE_CLASS_ALL: AwsCloudFrontSpec.PriceClass
    class Origin(_message.Message):
        __slots__ = ("domain_name", "origin_path", "is_default")
        DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_PATH_FIELD_NUMBER: _ClassVar[int]
        IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
        domain_name: str
        origin_path: str
        is_default: bool
        def __init__(self, domain_name: _Optional[str] = ..., origin_path: _Optional[str] = ..., is_default: bool = ...) -> None: ...
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ALIASES_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_ARN_FIELD_NUMBER: _ClassVar[int]
    PRICE_CLASS_FIELD_NUMBER: _ClassVar[int]
    ORIGINS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ROOT_OBJECT_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    aliases: _containers.RepeatedScalarFieldContainer[str]
    certificate_arn: str
    price_class: AwsCloudFrontSpec.PriceClass
    origins: _containers.RepeatedCompositeFieldContainer[AwsCloudFrontSpec.Origin]
    default_root_object: str
    def __init__(self, enabled: bool = ..., aliases: _Optional[_Iterable[str]] = ..., certificate_arn: _Optional[str] = ..., price_class: _Optional[_Union[AwsCloudFrontSpec.PriceClass, str]] = ..., origins: _Optional[_Iterable[_Union[AwsCloudFrontSpec.Origin, _Mapping]]] = ..., default_root_object: _Optional[str] = ...) -> None: ...
