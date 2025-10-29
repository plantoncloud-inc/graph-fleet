from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestApiResourceEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEST_EVENT_TYPE_UNSPECIFIED: _ClassVar[TestApiResourceEventType]
    TEST_EVENT_TYPE_STATE_CREATED: _ClassVar[TestApiResourceEventType]
    TEST_EVENT_TYPE_STATE_UPDATED: _ClassVar[TestApiResourceEventType]

class CloudProviderTest(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLOUD_PROVIDER_TEST_UNSPECIFIED: _ClassVar[CloudProviderTest]
    CLOUD_PROVIDER_TEST_GCP: _ClassVar[CloudProviderTest]
    CLOUD_PROVIDER_TEST_AWS: _ClassVar[CloudProviderTest]
TEST_EVENT_TYPE_UNSPECIFIED: TestApiResourceEventType
TEST_EVENT_TYPE_STATE_CREATED: TestApiResourceEventType
TEST_EVENT_TYPE_STATE_UPDATED: TestApiResourceEventType
CLOUD_PROVIDER_TEST_UNSPECIFIED: CloudProviderTest
CLOUD_PROVIDER_TEST_GCP: CloudProviderTest
CLOUD_PROVIDER_TEST_AWS: CloudProviderTest

class EnumFieldsTest(_message.Message):
    __slots__ = ("event_type",)
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    event_type: TestApiResourceEventType
    def __init__(self, event_type: _Optional[_Union[TestApiResourceEventType, str]] = ...) -> None: ...
