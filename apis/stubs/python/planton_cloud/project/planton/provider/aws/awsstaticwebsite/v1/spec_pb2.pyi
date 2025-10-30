from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsStaticWebsiteSpec(_message.Message):
    __slots__ = ("enable_cdn", "route53_zone_id", "domain_aliases", "certificate_arn", "content_bucket_arn", "content_prefix", "is_spa", "index_document", "error_document", "default_ttl_seconds", "max_ttl_seconds", "min_ttl_seconds", "compress", "ipv6_enabled", "price_class", "logging", "tags")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ENABLE_CDN_FIELD_NUMBER: _ClassVar[int]
    ROUTE53_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_ALIASES_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_ARN_FIELD_NUMBER: _ClassVar[int]
    CONTENT_BUCKET_ARN_FIELD_NUMBER: _ClassVar[int]
    CONTENT_PREFIX_FIELD_NUMBER: _ClassVar[int]
    IS_SPA_FIELD_NUMBER: _ClassVar[int]
    INDEX_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MAX_TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MIN_TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    COMPRESS_FIELD_NUMBER: _ClassVar[int]
    IPV6_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PRICE_CLASS_FIELD_NUMBER: _ClassVar[int]
    LOGGING_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    enable_cdn: bool
    route53_zone_id: _foreign_key_pb2.StringValueOrRef
    domain_aliases: _containers.RepeatedScalarFieldContainer[str]
    certificate_arn: _foreign_key_pb2.StringValueOrRef
    content_bucket_arn: _foreign_key_pb2.StringValueOrRef
    content_prefix: str
    is_spa: bool
    index_document: str
    error_document: str
    default_ttl_seconds: int
    max_ttl_seconds: int
    min_ttl_seconds: int
    compress: bool
    ipv6_enabled: bool
    price_class: str
    logging: AwsStaticWebsiteLogging
    tags: _containers.ScalarMap[str, str]
    def __init__(self, enable_cdn: bool = ..., route53_zone_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., domain_aliases: _Optional[_Iterable[str]] = ..., certificate_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., content_bucket_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., content_prefix: _Optional[str] = ..., is_spa: bool = ..., index_document: _Optional[str] = ..., error_document: _Optional[str] = ..., default_ttl_seconds: _Optional[int] = ..., max_ttl_seconds: _Optional[int] = ..., min_ttl_seconds: _Optional[int] = ..., compress: bool = ..., ipv6_enabled: bool = ..., price_class: _Optional[str] = ..., logging: _Optional[_Union[AwsStaticWebsiteLogging, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class AwsStaticWebsiteLogging(_message.Message):
    __slots__ = ("s3_enabled", "s3_target_bucket_arn", "s3_target_prefix", "cdn_enabled")
    S3_ENABLED_FIELD_NUMBER: _ClassVar[int]
    S3_TARGET_BUCKET_ARN_FIELD_NUMBER: _ClassVar[int]
    S3_TARGET_PREFIX_FIELD_NUMBER: _ClassVar[int]
    CDN_ENABLED_FIELD_NUMBER: _ClassVar[int]
    s3_enabled: bool
    s3_target_bucket_arn: _foreign_key_pb2.StringValueOrRef
    s3_target_prefix: str
    cdn_enabled: bool
    def __init__(self, s3_enabled: bool = ..., s3_target_bucket_arn: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., s3_target_prefix: _Optional[str] = ..., cdn_enabled: bool = ...) -> None: ...
