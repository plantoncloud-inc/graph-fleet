from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlowControlPolicySpec(_message.Message):
    __slots__ = ("selector", "flow_control")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    FLOW_CONTROL_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    flow_control: StackJobFlowControl
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., flow_control: _Optional[_Union[StackJobFlowControl, _Mapping]] = ...) -> None: ...

class StackJobFlowControl(_message.Message):
    __slots__ = ("is_manual", "disable_on_lifecycle_events", "skip_refresh", "preview_before_update_or_destroy", "pause_between_preview_and_update_or_destroy")
    IS_MANUAL_FIELD_NUMBER: _ClassVar[int]
    DISABLE_ON_LIFECYCLE_EVENTS_FIELD_NUMBER: _ClassVar[int]
    SKIP_REFRESH_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_BEFORE_UPDATE_OR_DESTROY_FIELD_NUMBER: _ClassVar[int]
    PAUSE_BETWEEN_PREVIEW_AND_UPDATE_OR_DESTROY_FIELD_NUMBER: _ClassVar[int]
    is_manual: bool
    disable_on_lifecycle_events: bool
    skip_refresh: bool
    preview_before_update_or_destroy: bool
    pause_between_preview_and_update_or_destroy: bool
    def __init__(self, is_manual: bool = ..., disable_on_lifecycle_events: bool = ..., skip_refresh: bool = ..., preview_before_update_or_destroy: bool = ..., pause_between_preview_and_update_or_destroy: bool = ...) -> None: ...
