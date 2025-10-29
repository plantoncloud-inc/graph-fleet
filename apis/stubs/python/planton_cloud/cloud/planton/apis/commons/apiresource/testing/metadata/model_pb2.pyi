from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResourceIdExtractionTestWithOutIdPrefix(_message.Message):
    __slots__ = ("org_name", "org")
    ORG_NAME_FIELD_NUMBER: _ClassVar[int]
    ORG_FIELD_NUMBER: _ClassVar[int]
    org_name: str
    org: str
    def __init__(self, org_name: _Optional[str] = ..., org: _Optional[str] = ...) -> None: ...

class ApiResourceIdExtractionTestWithIdPrefix(_message.Message):
    __slots__ = ("microservice_name", "microservice_id")
    MICROSERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    MICROSERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    microservice_name: str
    microservice_id: str
    def __init__(self, microservice_name: _Optional[str] = ..., microservice_id: _Optional[str] = ...) -> None: ...

class RegexNameFieldProtoValidateTest(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: MetadataTest
    def __init__(self, metadata: _Optional[_Union[MetadataTest, _Mapping]] = ...) -> None: ...

class SplitRegexNameFieldProtoValidateTest(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: MetadataTest
    def __init__(self, metadata: _Optional[_Union[MetadataTest, _Mapping]] = ...) -> None: ...

class MetadataTest(_message.Message):
    __slots__ = ("name", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    def __init__(self, name: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class IsRequiredFieldProtoValidateTest(_message.Message):
    __slots__ = ("is_required_field",)
    IS_REQUIRED_FIELD_FIELD_NUMBER: _ClassVar[int]
    is_required_field: str
    def __init__(self, is_required_field: _Optional[str] = ...) -> None: ...
