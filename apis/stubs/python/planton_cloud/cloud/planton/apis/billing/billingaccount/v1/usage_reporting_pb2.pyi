import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDeploymentMinutesByContextInput(_message.Message):
    __slots__ = ("org", "env")
    ORG_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    org: str
    env: str
    def __init__(self, org: _Optional[str] = ..., env: _Optional[str] = ...) -> None: ...

class UsageMinutesCurrentAndPreviousMonth(_message.Message):
    __slots__ = ("current_month_minutes", "previous_month_minutes")
    CURRENT_MONTH_MINUTES_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_MONTH_MINUTES_FIELD_NUMBER: _ClassVar[int]
    current_month_minutes: float
    previous_month_minutes: float
    def __init__(self, current_month_minutes: _Optional[float] = ..., previous_month_minutes: _Optional[float] = ...) -> None: ...

class SyncAutomationRunnerJobsInput(_message.Message):
    __slots__ = ("org", "start_time", "end_time")
    ORG_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    org: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, org: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ReportAutomationRunnerUsageInput(_message.Message):
    __slots__ = ("org", "start_time", "end_time")
    ORG_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    org: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, org: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ReportSeatUsageInput(_message.Message):
    __slots__ = ("org",)
    ORG_FIELD_NUMBER: _ClassVar[int]
    org: str
    def __init__(self, org: _Optional[str] = ...) -> None: ...
