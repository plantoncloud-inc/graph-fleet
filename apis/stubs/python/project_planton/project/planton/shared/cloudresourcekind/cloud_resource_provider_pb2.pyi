from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CloudResourceProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    cloud_resource_provider_unspecified: _ClassVar[CloudResourceProvider]
    _test: _ClassVar[CloudResourceProvider]
    atlas: _ClassVar[CloudResourceProvider]
    aws: _ClassVar[CloudResourceProvider]
    azure: _ClassVar[CloudResourceProvider]
    civo: _ClassVar[CloudResourceProvider]
    cloudflare: _ClassVar[CloudResourceProvider]
    confluent: _ClassVar[CloudResourceProvider]
    digital_ocean: _ClassVar[CloudResourceProvider]
    gcp: _ClassVar[CloudResourceProvider]
    kubernetes: _ClassVar[CloudResourceProvider]
    snowflake: _ClassVar[CloudResourceProvider]
cloud_resource_provider_unspecified: CloudResourceProvider
_test: CloudResourceProvider
atlas: CloudResourceProvider
aws: CloudResourceProvider
azure: CloudResourceProvider
civo: CloudResourceProvider
cloudflare: CloudResourceProvider
confluent: CloudResourceProvider
digital_ocean: CloudResourceProvider
gcp: CloudResourceProvider
kubernetes: CloudResourceProvider
snowflake: CloudResourceProvider
PROVIDER_META_FIELD_NUMBER: _ClassVar[int]
provider_meta: _descriptor.FieldDescriptor

class CloudResourceProviderMeta(_message.Message):
    __slots__ = ("group", "display_name")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    group: str
    display_name: str
    def __init__(self, group: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...
