from project.planton.provider.kubernetes import provider_pb2 as _provider_pb2
from project.planton.provider.kubernetes.workload.clickhousekubernetes.v1 import api_pb2 as _api_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClickHouseKubernetesStackInput(_message.Message):
    __slots__ = ("target", "provider_config", "kubernetes_namespace")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    target: _api_pb2.ClickHouseKubernetes
    provider_config: _provider_pb2.KubernetesProviderConfig
    kubernetes_namespace: str
    def __init__(self, target: _Optional[_Union[_api_pb2.ClickHouseKubernetes, _Mapping]] = ..., provider_config: _Optional[_Union[_provider_pb2.KubernetesProviderConfig, _Mapping]] = ..., kubernetes_namespace: _Optional[str] = ...) -> None: ...
