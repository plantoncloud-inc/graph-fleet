from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.billing.billingaccount.v1 import enum_pb2 as _enum_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubscriptionInput(_message.Message):
    __slots__ = ("org", "subscription_plan")
    ORG_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_PLAN_FIELD_NUMBER: _ClassVar[int]
    org: str
    subscription_plan: _enum_pb2.SubscriptionPlan
    def __init__(self, org: _Optional[str] = ..., subscription_plan: _Optional[_Union[_enum_pb2.SubscriptionPlan, str]] = ...) -> None: ...

class BillingNotification(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class BillingPortalSessionUrl(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class CheckBillingStatusResponse(_message.Message):
    __slots__ = ("is_valid", "message")
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    message: str
    def __init__(self, is_valid: bool = ..., message: _Optional[str] = ...) -> None: ...
