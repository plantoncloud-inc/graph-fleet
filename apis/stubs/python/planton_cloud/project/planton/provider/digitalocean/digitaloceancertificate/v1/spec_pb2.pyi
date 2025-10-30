from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanCertificateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    letsEncrypt: _ClassVar[DigitalOceanCertificateType]
    custom: _ClassVar[DigitalOceanCertificateType]
letsEncrypt: DigitalOceanCertificateType
custom: DigitalOceanCertificateType

class DigitalOceanCertificateSpec(_message.Message):
    __slots__ = ("certificate_name", "type", "lets_encrypt", "custom", "description", "tags")
    CERTIFICATE_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LETS_ENCRYPT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    certificate_name: str
    type: DigitalOceanCertificateType
    lets_encrypt: DigitalOceanCertificateLetsEncryptParams
    custom: DigitalOceanCertificateCustomParams
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, certificate_name: _Optional[str] = ..., type: _Optional[_Union[DigitalOceanCertificateType, str]] = ..., lets_encrypt: _Optional[_Union[DigitalOceanCertificateLetsEncryptParams, _Mapping]] = ..., custom: _Optional[_Union[DigitalOceanCertificateCustomParams, _Mapping]] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class DigitalOceanCertificateLetsEncryptParams(_message.Message):
    __slots__ = ("domains", "disable_auto_renew")
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_AUTO_RENEW_FIELD_NUMBER: _ClassVar[int]
    domains: _containers.RepeatedScalarFieldContainer[str]
    disable_auto_renew: bool
    def __init__(self, domains: _Optional[_Iterable[str]] = ..., disable_auto_renew: bool = ...) -> None: ...

class DigitalOceanCertificateCustomParams(_message.Message):
    __slots__ = ("leaf_certificate", "private_key", "certificate_chain")
    LEAF_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_CHAIN_FIELD_NUMBER: _ClassVar[int]
    leaf_certificate: str
    private_key: str
    certificate_chain: str
    def __init__(self, leaf_certificate: _Optional[str] = ..., private_key: _Optional[str] = ..., certificate_chain: _Optional[str] = ...) -> None: ...
