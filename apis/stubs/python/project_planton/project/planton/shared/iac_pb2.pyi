from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class IacProvisioner(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    iac_provisioner_unspecified: _ClassVar[IacProvisioner]
    terraform: _ClassVar[IacProvisioner]
    pulumi: _ClassVar[IacProvisioner]
iac_provisioner_unspecified: IacProvisioner
terraform: IacProvisioner
pulumi: IacProvisioner
