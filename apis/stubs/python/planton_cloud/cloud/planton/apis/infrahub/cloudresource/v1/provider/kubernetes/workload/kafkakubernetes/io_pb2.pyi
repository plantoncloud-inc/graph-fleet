from buf.validate import validate_pb2 as _validate_pb2
from project.planton.provider.kubernetes.workload.kafkakubernetes.v1 import spec_pb2 as _spec_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KafkaKubernetesId(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class AddOrUpdateKafkaTopicInput(_message.Message):
    __slots__ = ("kafka_kubernetes_id", "kafka_topic", "version_message")
    KAFKA_KUBERNETES_ID_FIELD_NUMBER: _ClassVar[int]
    KAFKA_TOPIC_FIELD_NUMBER: _ClassVar[int]
    VERSION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    kafka_kubernetes_id: str
    kafka_topic: _spec_pb2.KafkaTopic
    version_message: str
    def __init__(self, kafka_kubernetes_id: _Optional[str] = ..., kafka_topic: _Optional[_Union[_spec_pb2.KafkaTopic, _Mapping]] = ..., version_message: _Optional[str] = ...) -> None: ...

class DeleteOrRestoreKafkaTopicInput(_message.Message):
    __slots__ = ("kafka_kubernetes_id", "kafka_topic_name", "version_message")
    KAFKA_KUBERNETES_ID_FIELD_NUMBER: _ClassVar[int]
    KAFKA_TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    kafka_kubernetes_id: str
    kafka_topic_name: str
    version_message: str
    def __init__(self, kafka_kubernetes_id: _Optional[str] = ..., kafka_topic_name: _Optional[str] = ..., version_message: _Optional[str] = ...) -> None: ...

class KafkaTopicQueryInput(_message.Message):
    __slots__ = ("kafka_kubernetes_id", "kafka_topic")
    KAFKA_KUBERNETES_ID_FIELD_NUMBER: _ClassVar[int]
    KAFKA_TOPIC_FIELD_NUMBER: _ClassVar[int]
    kafka_kubernetes_id: str
    kafka_topic: _spec_pb2.KafkaTopic
    def __init__(self, kafka_kubernetes_id: _Optional[str] = ..., kafka_topic: _Optional[_Union[_spec_pb2.KafkaTopic, _Mapping]] = ...) -> None: ...
