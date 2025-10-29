import datetime

from cloud.planton.apis.billing.billingaccount.v1 import enum_pb2 as _enum_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BillingAccountSpec(_message.Message):
    __slots__ = ("organization_created_by", "description", "customer_id", "subscription_id", "subscription_plan", "trial_end_date", "is_default_payment_method_exists", "next_billing_date", "is_cancel_at_period_end", "current_billing_start_date", "subscription_status")
    ORGANIZATION_CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_PLAN_FIELD_NUMBER: _ClassVar[int]
    TRIAL_END_DATE_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_PAYMENT_METHOD_EXISTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_BILLING_DATE_FIELD_NUMBER: _ClassVar[int]
    IS_CANCEL_AT_PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    CURRENT_BILLING_START_DATE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    organization_created_by: str
    description: str
    customer_id: str
    subscription_id: str
    subscription_plan: _enum_pb2.SubscriptionPlan
    trial_end_date: _timestamp_pb2.Timestamp
    is_default_payment_method_exists: bool
    next_billing_date: _timestamp_pb2.Timestamp
    is_cancel_at_period_end: bool
    current_billing_start_date: _timestamp_pb2.Timestamp
    subscription_status: str
    def __init__(self, organization_created_by: _Optional[str] = ..., description: _Optional[str] = ..., customer_id: _Optional[str] = ..., subscription_id: _Optional[str] = ..., subscription_plan: _Optional[_Union[_enum_pb2.SubscriptionPlan, str]] = ..., trial_end_date: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_default_payment_method_exists: bool = ..., next_billing_date: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_cancel_at_period_end: bool = ..., current_billing_start_date: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., subscription_status: _Optional[str] = ...) -> None: ...
