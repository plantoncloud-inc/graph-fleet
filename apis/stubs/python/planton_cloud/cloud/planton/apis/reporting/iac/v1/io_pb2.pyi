import datetime

from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource.apiresourcekind import api_resource_kind_pb2 as _api_resource_kind_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TotalIacResourceCount(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class IacResourceCountTimeSeries(_message.Message):
    __slots__ = ("interval_timestamp", "resource_count")
    INTERVAL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    interval_timestamp: _timestamp_pb2.Timestamp
    resource_count: float
    def __init__(self, interval_timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., resource_count: _Optional[float] = ...) -> None: ...

class IacResourceCountTimeSeriesList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[IacResourceCountTimeSeries]
    def __init__(self, entries: _Optional[_Iterable[_Union[IacResourceCountTimeSeries, _Mapping]]] = ...) -> None: ...

class GetIacResourceCountTimeSeriesByContextInput(_message.Message):
    __slots__ = ("org", "env", "start_timestamp", "end_timestamp")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    start_timestamp: _timestamp_pb2.Timestamp
    end_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., start_timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetIacResourceCountTimeSeriesByResourceIdInput(_message.Message):
    __slots__ = ("resource_kind", "resource_id", "start_timestamp", "end_timestamp")
    RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    resource_kind: _api_resource_kind_pb2.ApiResourceKind
    resource_id: str
    start_timestamp: _timestamp_pb2.Timestamp
    end_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., resource_id: _Optional[str] = ..., start_timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetIacResourceCountByContextInput(_message.Message):
    __slots__ = ("org", "env")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...

class IacResourceCountDetailed(_message.Message):
    __slots__ = ("org", "env", "api_resource_id", "api_resource_kind", "resource_count")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    API_RESOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    api_resource_id: str
    api_resource_kind: _api_resource_kind_pb2.ApiResourceKind
    resource_count: int
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ..., api_resource_id: _Optional[str] = ..., api_resource_kind: _Optional[_Union[_api_resource_kind_pb2.ApiResourceKind, str]] = ..., resource_count: _Optional[int] = ...) -> None: ...

class IacResourceCountDetailedList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[IacResourceCountDetailed]
    def __init__(self, entries: _Optional[_Iterable[_Union[IacResourceCountDetailed, _Mapping]]] = ...) -> None: ...
