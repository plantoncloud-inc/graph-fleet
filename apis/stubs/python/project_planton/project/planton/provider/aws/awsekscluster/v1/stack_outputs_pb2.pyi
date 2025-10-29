from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsEksClusterStackOutputs(_message.Message):
    __slots__ = ("endpoint", "cluster_ca_certificate", "cluster_security_group_id", "oidc_issuer_url", "cluster_arn", "name")
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CA_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_SECURITY_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    OIDC_ISSUER_URL_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ARN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    endpoint: str
    cluster_ca_certificate: str
    cluster_security_group_id: str
    oidc_issuer_url: str
    cluster_arn: str
    name: str
    def __init__(self, endpoint: _Optional[str] = ..., cluster_ca_certificate: _Optional[str] = ..., cluster_security_group_id: _Optional[str] = ..., oidc_issuer_url: _Optional[str] = ..., cluster_arn: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
