from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalOceanFirewallSpec(_message.Message):
    __slots__ = ("name", "inbound_rules", "outbound_rules", "droplet_ids", "tags")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INBOUND_RULES_FIELD_NUMBER: _ClassVar[int]
    OUTBOUND_RULES_FIELD_NUMBER: _ClassVar[int]
    DROPLET_IDS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    inbound_rules: _containers.RepeatedCompositeFieldContainer[DigitalOceanFirewallInboundRule]
    outbound_rules: _containers.RepeatedCompositeFieldContainer[DigitalOceanFirewallOutboundRule]
    droplet_ids: _containers.RepeatedScalarFieldContainer[int]
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., inbound_rules: _Optional[_Iterable[_Union[DigitalOceanFirewallInboundRule, _Mapping]]] = ..., outbound_rules: _Optional[_Iterable[_Union[DigitalOceanFirewallOutboundRule, _Mapping]]] = ..., droplet_ids: _Optional[_Iterable[int]] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class DigitalOceanFirewallInboundRule(_message.Message):
    __slots__ = ("protocol", "port_range", "source_addresses", "source_droplet_ids", "source_tags", "source_kubernetes_ids", "source_load_balancer_uids")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_RANGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DROPLET_IDS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TAGS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_KUBERNETES_IDS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_LOAD_BALANCER_UIDS_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    port_range: str
    source_addresses: _containers.RepeatedScalarFieldContainer[str]
    source_droplet_ids: _containers.RepeatedScalarFieldContainer[int]
    source_tags: _containers.RepeatedScalarFieldContainer[str]
    source_kubernetes_ids: _containers.RepeatedScalarFieldContainer[str]
    source_load_balancer_uids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, protocol: _Optional[str] = ..., port_range: _Optional[str] = ..., source_addresses: _Optional[_Iterable[str]] = ..., source_droplet_ids: _Optional[_Iterable[int]] = ..., source_tags: _Optional[_Iterable[str]] = ..., source_kubernetes_ids: _Optional[_Iterable[str]] = ..., source_load_balancer_uids: _Optional[_Iterable[str]] = ...) -> None: ...

class DigitalOceanFirewallOutboundRule(_message.Message):
    __slots__ = ("protocol", "port_range", "destination_addresses", "destination_droplet_ids", "destination_tags", "destination_kubernetes_ids", "destination_load_balancer_uids")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_RANGE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_DROPLET_IDS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_TAGS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_KUBERNETES_IDS_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_LOAD_BALANCER_UIDS_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    port_range: str
    destination_addresses: _containers.RepeatedScalarFieldContainer[str]
    destination_droplet_ids: _containers.RepeatedScalarFieldContainer[int]
    destination_tags: _containers.RepeatedScalarFieldContainer[str]
    destination_kubernetes_ids: _containers.RepeatedScalarFieldContainer[str]
    destination_load_balancer_uids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, protocol: _Optional[str] = ..., port_range: _Optional[str] = ..., destination_addresses: _Optional[_Iterable[str]] = ..., destination_droplet_ids: _Optional[_Iterable[int]] = ..., destination_tags: _Optional[_Iterable[str]] = ..., destination_kubernetes_ids: _Optional[_Iterable[str]] = ..., destination_load_balancer_uids: _Optional[_Iterable[str]] = ...) -> None: ...
