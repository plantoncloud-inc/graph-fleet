from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class SubscriptionPlan(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    subscription_plan_unspecified: _ClassVar[SubscriptionPlan]
    free_plan: _ClassVar[SubscriptionPlan]
    plus_plan: _ClassVar[SubscriptionPlan]
    pro_plan: _ClassVar[SubscriptionPlan]
subscription_plan_unspecified: SubscriptionPlan
free_plan: SubscriptionPlan
plus_plan: SubscriptionPlan
pro_plan: SubscriptionPlan
