from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AwsDynamodbStackOutputs(_message.Message):
    __slots__ = ("table_name", "table_arn", "table_id", "stream_arn", "stream_label")
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_ARN_FIELD_NUMBER: _ClassVar[int]
    TABLE_ID_FIELD_NUMBER: _ClassVar[int]
    STREAM_ARN_FIELD_NUMBER: _ClassVar[int]
    STREAM_LABEL_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    table_arn: str
    table_id: str
    stream_arn: str
    stream_label: str
    def __init__(self, table_name: _Optional[str] = ..., table_arn: _Optional[str] = ..., table_id: _Optional[str] = ..., stream_arn: _Optional[str] = ..., stream_label: _Optional[str] = ...) -> None: ...
