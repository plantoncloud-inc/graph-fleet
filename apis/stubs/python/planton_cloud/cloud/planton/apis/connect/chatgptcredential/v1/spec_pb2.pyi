from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from project.planton.shared.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatGptCredentialSpec(_message.Message):
    __slots__ = ("selector", "api_url", "api_key", "model_id")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    API_URL_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    api_url: str
    api_key: str
    model_id: str
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., api_url: _Optional[str] = ..., api_key: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...
