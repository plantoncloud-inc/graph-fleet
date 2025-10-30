from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TemporalKubernetesStackOutputs(_message.Message):
    __slots__ = ("namespace", "frontend_service_name", "ui_service_name", "port_forward_frontend_command", "port_forward_ui_command", "frontend_endpoint", "web_ui_endpoint", "external_frontend_hostname", "external_ui_hostname")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FRONTEND_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    UI_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FORWARD_FRONTEND_COMMAND_FIELD_NUMBER: _ClassVar[int]
    PORT_FORWARD_UI_COMMAND_FIELD_NUMBER: _ClassVar[int]
    FRONTEND_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    WEB_UI_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FRONTEND_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_UI_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    frontend_service_name: str
    ui_service_name: str
    port_forward_frontend_command: str
    port_forward_ui_command: str
    frontend_endpoint: str
    web_ui_endpoint: str
    external_frontend_hostname: str
    external_ui_hostname: str
    def __init__(self, namespace: _Optional[str] = ..., frontend_service_name: _Optional[str] = ..., ui_service_name: _Optional[str] = ..., port_forward_frontend_command: _Optional[str] = ..., port_forward_ui_command: _Optional[str] = ..., frontend_endpoint: _Optional[str] = ..., web_ui_endpoint: _Optional[str] = ..., external_frontend_hostname: _Optional[str] = ..., external_ui_hostname: _Optional[str] = ...) -> None: ...
