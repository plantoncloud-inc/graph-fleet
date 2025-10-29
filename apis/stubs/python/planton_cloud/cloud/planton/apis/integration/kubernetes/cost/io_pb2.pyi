import datetime

from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from cloud.planton.apis.integration.kubernetes.cost import api_pb2 as _api_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CostAllocations(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.CostAllocation]
    def __init__(self, entries: _Optional[_Iterable[_Union[_api_pb2.CostAllocation, _Mapping]]] = ...) -> None: ...

class CostAllocationList(_message.Message):
    __slots__ = ("total_pages", "entries")
    TOTAL_PAGES_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    total_pages: int
    entries: _containers.RepeatedCompositeFieldContainer[_api_pb2.CostAllocation]
    def __init__(self, total_pages: _Optional[int] = ..., entries: _Optional[_Iterable[_Union[_api_pb2.CostAllocation, _Mapping]]] = ...) -> None: ...

class ListByCostAllocationFiltersInput(_message.Message):
    __slots__ = ("page_info", "start_ts", "end_ts", "env", "resource_kind", "resource_id")
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    START_TS_FIELD_NUMBER: _ClassVar[int]
    END_TS_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    page_info: _pagination_pb2.PageInfo
    start_ts: _timestamp_pb2.Timestamp
    end_ts: _timestamp_pb2.Timestamp
    env: str
    resource_kind: _api_resource_kind_pb2.ApiResourceKind
    resource_id: str
    def __init__(self, page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ..., start_ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., env: _Optional[str] = ..., resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., resource_id: _Optional[str] = ...) -> None: ...

class GetCostAggregateInput(_message.Message):
    __slots__ = ("resource_kind", "resource_id", "start_ts", "end_ts")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    START_TS_FIELD_NUMBER: _ClassVar[int]
    END_TS_FIELD_NUMBER: _ClassVar[int]
    resource_kind: _api_resource_kind_pb2.ApiResourceKind
    resource_id: str
    start_ts: _timestamp_pb2.Timestamp
    end_ts: _timestamp_pb2.Timestamp
    def __init__(self, resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., resource_id: _Optional[str] = ..., start_ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CostAggregate(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...
