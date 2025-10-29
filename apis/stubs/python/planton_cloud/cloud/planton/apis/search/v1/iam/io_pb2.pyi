from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.rpc import pagination_pb2 as _pagination_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchIdentityAccountByEmailInput(_message.Message):
    __slots__ = ("org", "search_text", "page_info")
    ORG_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TEXT_FIELD_NUMBER: _ClassVar[int]
    PAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    org: str
    search_text: str
    page_info: _pagination_pb2.PageInfo
    def __init__(self, org: _Optional[str] = ..., search_text: _Optional[str] = ..., page_info: _Optional[_Union[_pagination_pb2.PageInfo, _Mapping]] = ...) -> None: ...
