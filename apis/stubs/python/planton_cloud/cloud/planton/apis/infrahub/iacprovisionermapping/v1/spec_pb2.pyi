from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from project.planton.shared import iac_pb2 as _iac_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IacProvisionerMappingSpec(_message.Message):
    __slots__ = ("selector", "provisioner")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PROVISIONER_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    provisioner: _iac_pb2.IacProvisioner
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., provisioner: _Optional[_Union[_iac_pb2.IacProvisioner, str]] = ...) -> None: ...
