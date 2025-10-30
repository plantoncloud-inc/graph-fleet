from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsCertManagerCertStackOutputs(_message.Message):
    __slots__ = ("cert_arn", "certificate_domain_name")
    CERT_ARN_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    cert_arn: str
    certificate_domain_name: str
    def __init__(self, cert_arn: _Optional[str] = ..., certificate_domain_name: _Optional[str] = ...) -> None: ...
