from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class IdentityAccountType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    identity_account_unspecified: _ClassVar[IdentityAccountType]
    user: _ClassVar[IdentityAccountType]
    machine: _ClassVar[IdentityAccountType]

class MicroserviceIdentityAccountActorIdValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    microservice_identity_account_actor_id_unspecified: _ClassVar[MicroserviceIdentityAccountActorIdValue]
    system: _ClassVar[MicroserviceIdentityAccountActorIdValue]
identity_account_unspecified: IdentityAccountType
user: IdentityAccountType
machine: IdentityAccountType
microservice_identity_account_actor_id_unspecified: MicroserviceIdentityAccountActorIdValue
system: MicroserviceIdentityAccountActorIdValue
