from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsDynamodbSpec(_message.Message):
    __slots__ = ("billing_mode", "provisioned_throughput", "attribute_definitions", "key_schema", "global_secondary_indexes", "local_secondary_indexes", "ttl", "stream_enabled", "stream_view_type", "point_in_time_recovery_enabled", "server_side_encryption", "table_class", "deletion_protection_enabled", "contributor_insights_enabled")
    class BillingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BILLING_MODE_UNSPECIFIED: _ClassVar[AwsDynamodbSpec.BillingMode]
        BILLING_MODE_PROVISIONED: _ClassVar[AwsDynamodbSpec.BillingMode]
        BILLING_MODE_PAY_PER_REQUEST: _ClassVar[AwsDynamodbSpec.BillingMode]
    BILLING_MODE_UNSPECIFIED: AwsDynamodbSpec.BillingMode
    BILLING_MODE_PROVISIONED: AwsDynamodbSpec.BillingMode
    BILLING_MODE_PAY_PER_REQUEST: AwsDynamodbSpec.BillingMode
    class AttributeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ATTRIBUTE_TYPE_UNSPECIFIED: _ClassVar[AwsDynamodbSpec.AttributeType]
        ATTRIBUTE_TYPE_S: _ClassVar[AwsDynamodbSpec.AttributeType]
        ATTRIBUTE_TYPE_N: _ClassVar[AwsDynamodbSpec.AttributeType]
        ATTRIBUTE_TYPE_B: _ClassVar[AwsDynamodbSpec.AttributeType]
    ATTRIBUTE_TYPE_UNSPECIFIED: AwsDynamodbSpec.AttributeType
    ATTRIBUTE_TYPE_S: AwsDynamodbSpec.AttributeType
    ATTRIBUTE_TYPE_N: AwsDynamodbSpec.AttributeType
    ATTRIBUTE_TYPE_B: AwsDynamodbSpec.AttributeType
    class StreamViewType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STREAM_VIEW_TYPE_UNSPECIFIED: _ClassVar[AwsDynamodbSpec.StreamViewType]
        STREAM_VIEW_TYPE_KEYS_ONLY: _ClassVar[AwsDynamodbSpec.StreamViewType]
        STREAM_VIEW_TYPE_NEW_IMAGE: _ClassVar[AwsDynamodbSpec.StreamViewType]
        STREAM_VIEW_TYPE_OLD_IMAGE: _ClassVar[AwsDynamodbSpec.StreamViewType]
        STREAM_VIEW_TYPE_NEW_AND_OLD_IMAGES: _ClassVar[AwsDynamodbSpec.StreamViewType]
    STREAM_VIEW_TYPE_UNSPECIFIED: AwsDynamodbSpec.StreamViewType
    STREAM_VIEW_TYPE_KEYS_ONLY: AwsDynamodbSpec.StreamViewType
    STREAM_VIEW_TYPE_NEW_IMAGE: AwsDynamodbSpec.StreamViewType
    STREAM_VIEW_TYPE_OLD_IMAGE: AwsDynamodbSpec.StreamViewType
    STREAM_VIEW_TYPE_NEW_AND_OLD_IMAGES: AwsDynamodbSpec.StreamViewType
    class ProjectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PROJECTION_TYPE_UNSPECIFIED: _ClassVar[AwsDynamodbSpec.ProjectionType]
        PROJECTION_TYPE_ALL: _ClassVar[AwsDynamodbSpec.ProjectionType]
        PROJECTION_TYPE_KEYS_ONLY: _ClassVar[AwsDynamodbSpec.ProjectionType]
        PROJECTION_TYPE_INCLUDE: _ClassVar[AwsDynamodbSpec.ProjectionType]
    PROJECTION_TYPE_UNSPECIFIED: AwsDynamodbSpec.ProjectionType
    PROJECTION_TYPE_ALL: AwsDynamodbSpec.ProjectionType
    PROJECTION_TYPE_KEYS_ONLY: AwsDynamodbSpec.ProjectionType
    PROJECTION_TYPE_INCLUDE: AwsDynamodbSpec.ProjectionType
    class TableClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TABLE_CLASS_UNSPECIFIED: _ClassVar[AwsDynamodbSpec.TableClass]
        TABLE_CLASS_STANDARD: _ClassVar[AwsDynamodbSpec.TableClass]
        TABLE_CLASS_STANDARD_INFREQUENT_ACCESS: _ClassVar[AwsDynamodbSpec.TableClass]
    TABLE_CLASS_UNSPECIFIED: AwsDynamodbSpec.TableClass
    TABLE_CLASS_STANDARD: AwsDynamodbSpec.TableClass
    TABLE_CLASS_STANDARD_INFREQUENT_ACCESS: AwsDynamodbSpec.TableClass
    class AttributeDefinition(_message.Message):
        __slots__ = ("name", "type")
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: AwsDynamodbSpec.AttributeType
        def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[AwsDynamodbSpec.AttributeType, str]] = ...) -> None: ...
    class KeySchemaElement(_message.Message):
        __slots__ = ("attribute_name", "key_type")
        class KeyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            KEY_TYPE_UNSPECIFIED: _ClassVar[AwsDynamodbSpec.KeySchemaElement.KeyType]
            KEY_TYPE_HASH: _ClassVar[AwsDynamodbSpec.KeySchemaElement.KeyType]
            KEY_TYPE_RANGE: _ClassVar[AwsDynamodbSpec.KeySchemaElement.KeyType]
        KEY_TYPE_UNSPECIFIED: AwsDynamodbSpec.KeySchemaElement.KeyType
        KEY_TYPE_HASH: AwsDynamodbSpec.KeySchemaElement.KeyType
        KEY_TYPE_RANGE: AwsDynamodbSpec.KeySchemaElement.KeyType
        ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
        KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
        attribute_name: str
        key_type: AwsDynamodbSpec.KeySchemaElement.KeyType
        def __init__(self, attribute_name: _Optional[str] = ..., key_type: _Optional[_Union[AwsDynamodbSpec.KeySchemaElement.KeyType, str]] = ...) -> None: ...
    class Projection(_message.Message):
        __slots__ = ("type", "non_key_attributes")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        NON_KEY_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        type: AwsDynamodbSpec.ProjectionType
        non_key_attributes: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, type: _Optional[_Union[AwsDynamodbSpec.ProjectionType, str]] = ..., non_key_attributes: _Optional[_Iterable[str]] = ...) -> None: ...
    class ProvisionedThroughput(_message.Message):
        __slots__ = ("read_capacity_units", "write_capacity_units")
        READ_CAPACITY_UNITS_FIELD_NUMBER: _ClassVar[int]
        WRITE_CAPACITY_UNITS_FIELD_NUMBER: _ClassVar[int]
        read_capacity_units: int
        write_capacity_units: int
        def __init__(self, read_capacity_units: _Optional[int] = ..., write_capacity_units: _Optional[int] = ...) -> None: ...
    class GlobalSecondaryIndex(_message.Message):
        __slots__ = ("name", "key_schema", "projection", "provisioned_throughput")
        NAME_FIELD_NUMBER: _ClassVar[int]
        KEY_SCHEMA_FIELD_NUMBER: _ClassVar[int]
        PROJECTION_FIELD_NUMBER: _ClassVar[int]
        PROVISIONED_THROUGHPUT_FIELD_NUMBER: _ClassVar[int]
        name: str
        key_schema: _containers.RepeatedCompositeFieldContainer[AwsDynamodbSpec.KeySchemaElement]
        projection: AwsDynamodbSpec.Projection
        provisioned_throughput: AwsDynamodbSpec.ProvisionedThroughput
        def __init__(self, name: _Optional[str] = ..., key_schema: _Optional[_Iterable[_Union[AwsDynamodbSpec.KeySchemaElement, _Mapping]]] = ..., projection: _Optional[_Union[AwsDynamodbSpec.Projection, _Mapping]] = ..., provisioned_throughput: _Optional[_Union[AwsDynamodbSpec.ProvisionedThroughput, _Mapping]] = ...) -> None: ...
    class LocalSecondaryIndex(_message.Message):
        __slots__ = ("name", "key_schema", "projection")
        NAME_FIELD_NUMBER: _ClassVar[int]
        KEY_SCHEMA_FIELD_NUMBER: _ClassVar[int]
        PROJECTION_FIELD_NUMBER: _ClassVar[int]
        name: str
        key_schema: _containers.RepeatedCompositeFieldContainer[AwsDynamodbSpec.KeySchemaElement]
        projection: AwsDynamodbSpec.Projection
        def __init__(self, name: _Optional[str] = ..., key_schema: _Optional[_Iterable[_Union[AwsDynamodbSpec.KeySchemaElement, _Mapping]]] = ..., projection: _Optional[_Union[AwsDynamodbSpec.Projection, _Mapping]] = ...) -> None: ...
    class ServerSideEncryption(_message.Message):
        __slots__ = ("enabled", "kms_key_arn")
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        KMS_KEY_ARN_FIELD_NUMBER: _ClassVar[int]
        enabled: bool
        kms_key_arn: str
        def __init__(self, enabled: bool = ..., kms_key_arn: _Optional[str] = ...) -> None: ...
    class TimeToLive(_message.Message):
        __slots__ = ("enabled", "attribute_name")
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
        enabled: bool
        attribute_name: str
        def __init__(self, enabled: bool = ..., attribute_name: _Optional[str] = ...) -> None: ...
    BILLING_MODE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_THROUGHPUT_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
    KEY_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_SECONDARY_INDEXES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_SECONDARY_INDEXES_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    STREAM_ENABLED_FIELD_NUMBER: _ClassVar[int]
    STREAM_VIEW_TYPE_FIELD_NUMBER: _ClassVar[int]
    POINT_IN_TIME_RECOVERY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SERVER_SIDE_ENCRYPTION_FIELD_NUMBER: _ClassVar[int]
    TABLE_CLASS_FIELD_NUMBER: _ClassVar[int]
    DELETION_PROTECTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONTRIBUTOR_INSIGHTS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    billing_mode: AwsDynamodbSpec.BillingMode
    provisioned_throughput: AwsDynamodbSpec.ProvisionedThroughput
    attribute_definitions: _containers.RepeatedCompositeFieldContainer[AwsDynamodbSpec.AttributeDefinition]
    key_schema: _containers.RepeatedCompositeFieldContainer[AwsDynamodbSpec.KeySchemaElement]
    global_secondary_indexes: _containers.RepeatedCompositeFieldContainer[AwsDynamodbSpec.GlobalSecondaryIndex]
    local_secondary_indexes: _containers.RepeatedCompositeFieldContainer[AwsDynamodbSpec.LocalSecondaryIndex]
    ttl: AwsDynamodbSpec.TimeToLive
    stream_enabled: bool
    stream_view_type: AwsDynamodbSpec.StreamViewType
    point_in_time_recovery_enabled: bool
    server_side_encryption: AwsDynamodbSpec.ServerSideEncryption
    table_class: AwsDynamodbSpec.TableClass
    deletion_protection_enabled: bool
    contributor_insights_enabled: bool
    def __init__(self, billing_mode: _Optional[_Union[AwsDynamodbSpec.BillingMode, str]] = ..., provisioned_throughput: _Optional[_Union[AwsDynamodbSpec.ProvisionedThroughput, _Mapping]] = ..., attribute_definitions: _Optional[_Iterable[_Union[AwsDynamodbSpec.AttributeDefinition, _Mapping]]] = ..., key_schema: _Optional[_Iterable[_Union[AwsDynamodbSpec.KeySchemaElement, _Mapping]]] = ..., global_secondary_indexes: _Optional[_Iterable[_Union[AwsDynamodbSpec.GlobalSecondaryIndex, _Mapping]]] = ..., local_secondary_indexes: _Optional[_Iterable[_Union[AwsDynamodbSpec.LocalSecondaryIndex, _Mapping]]] = ..., ttl: _Optional[_Union[AwsDynamodbSpec.TimeToLive, _Mapping]] = ..., stream_enabled: bool = ..., stream_view_type: _Optional[_Union[AwsDynamodbSpec.StreamViewType, str]] = ..., point_in_time_recovery_enabled: bool = ..., server_side_encryption: _Optional[_Union[AwsDynamodbSpec.ServerSideEncryption, _Mapping]] = ..., table_class: _Optional[_Union[AwsDynamodbSpec.TableClass, str]] = ..., deletion_protection_enabled: bool = ..., contributor_insights_enabled: bool = ...) -> None: ...
