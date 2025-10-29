from buf.validate import validate_pb2 as _validate_pb2
from project.planton.shared.foreignkey.v1 import foreign_key_pb2 as _foreign_key_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CivoFirewallSpec(_message.Message):
    __slots__ = ("name", "network_id", "inbound_rules", "outbound_rules", "tags")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NETWORK_ID_FIELD_NUMBER: _ClassVar[int]
    INBOUND_RULES_FIELD_NUMBER: _ClassVar[int]
    OUTBOUND_RULES_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    network_id: _foreign_key_pb2.StringValueOrRef
    inbound_rules: _containers.RepeatedCompositeFieldContainer[CivoFirewallInboundRule]
    outbound_rules: _containers.RepeatedCompositeFieldContainer[CivoFirewallOutboundRule]
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., network_id: _Optional[_Union[_foreign_key_pb2.StringValueOrRef, _Mapping]] = ..., inbound_rules: _Optional[_Iterable[_Union[CivoFirewallInboundRule, _Mapping]]] = ..., outbound_rules: _Optional[_Iterable[_Union[CivoFirewallOutboundRule, _Mapping]]] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class CivoFirewallInboundRule(_message.Message):
    __slots__ = ("protocol", "port_range", "cidrs", "action", "label")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_RANGE_FIELD_NUMBER: _ClassVar[int]
    CIDRS_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    port_range: str
    cidrs: _containers.RepeatedScalarFieldContainer[str]
    action: str
    label: str
    def __init__(self, protocol: _Optional[str] = ..., port_range: _Optional[str] = ..., cidrs: _Optional[_Iterable[str]] = ..., action: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...

class CivoFirewallOutboundRule(_message.Message):
    __slots__ = ("protocol", "port_range", "cidrs", "action", "label")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_RANGE_FIELD_NUMBER: _ClassVar[int]
    CIDRS_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    port_range: str
    cidrs: _containers.RepeatedScalarFieldContainer[str]
    action: str
    label: str
    def __init__(self, protocol: _Optional[str] = ..., port_range: _Optional[str] = ..., cidrs: _Optional[_Iterable[str]] = ..., action: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...
