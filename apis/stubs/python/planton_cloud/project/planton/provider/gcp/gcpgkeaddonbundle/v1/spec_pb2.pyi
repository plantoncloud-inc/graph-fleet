from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GcpGkeAddonBundleSpec(_message.Message):
    __slots__ = ("cluster_project_id", "istio", "install_postgres_operator", "install_kafka_operator", "install_solr_operator", "install_kubecost", "install_ingress_nginx", "install_cert_manager", "install_external_dns", "install_external_secrets", "install_elastic_operator", "install_keycloak_operator")
    CLUSTER_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ISTIO_FIELD_NUMBER: _ClassVar[int]
    INSTALL_POSTGRES_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    INSTALL_KAFKA_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    INSTALL_SOLR_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    INSTALL_KUBECOST_FIELD_NUMBER: _ClassVar[int]
    INSTALL_INGRESS_NGINX_FIELD_NUMBER: _ClassVar[int]
    INSTALL_CERT_MANAGER_FIELD_NUMBER: _ClassVar[int]
    INSTALL_EXTERNAL_DNS_FIELD_NUMBER: _ClassVar[int]
    INSTALL_EXTERNAL_SECRETS_FIELD_NUMBER: _ClassVar[int]
    INSTALL_ELASTIC_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    INSTALL_KEYCLOAK_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    cluster_project_id: str
    istio: GcpGkeAddonBundleIstio
    install_postgres_operator: bool
    install_kafka_operator: bool
    install_solr_operator: bool
    install_kubecost: bool
    install_ingress_nginx: bool
    install_cert_manager: bool
    install_external_dns: bool
    install_external_secrets: bool
    install_elastic_operator: bool
    install_keycloak_operator: bool
    def __init__(self, cluster_project_id: _Optional[str] = ..., istio: _Optional[_Union[GcpGkeAddonBundleIstio, _Mapping]] = ..., install_postgres_operator: bool = ..., install_kafka_operator: bool = ..., install_solr_operator: bool = ..., install_kubecost: bool = ..., install_ingress_nginx: bool = ..., install_cert_manager: bool = ..., install_external_dns: bool = ..., install_external_secrets: bool = ..., install_elastic_operator: bool = ..., install_keycloak_operator: bool = ...) -> None: ...

class GcpGkeAddonBundleIstio(_message.Message):
    __slots__ = ("enabled", "cluster_region", "sub_network_self_link")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_REGION_FIELD_NUMBER: _ClassVar[int]
    SUB_NETWORK_SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    cluster_region: str
    sub_network_self_link: str
    def __init__(self, enabled: bool = ..., cluster_region: _Optional[str] = ..., sub_network_self_link: _Optional[str] = ...) -> None: ...
