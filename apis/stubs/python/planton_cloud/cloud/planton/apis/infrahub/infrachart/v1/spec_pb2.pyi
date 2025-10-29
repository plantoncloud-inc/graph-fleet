from buf.validate import validate_pb2 as _validate_pb2
from cloud.planton.apis.commons.apiresource import field_options_pb2 as _field_options_pb2
from cloud.planton.apis.commons.apiresource import selector_pb2 as _selector_pb2
from cloud.planton.apis.infrahub.infrachart.v1 import param_pb2 as _param_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InfraChartSpec(_message.Message):
    __slots__ = ("selector", "description", "is_ready", "icon_url", "template_yaml_files", "values_yaml", "params", "web_links")
    class TemplateYamlFilesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_READY_FIELD_NUMBER: _ClassVar[int]
    ICON_URL_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_YAML_FILES_FIELD_NUMBER: _ClassVar[int]
    VALUES_YAML_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    WEB_LINKS_FIELD_NUMBER: _ClassVar[int]
    selector: _selector_pb2.ApiResourceSelector
    description: str
    is_ready: bool
    icon_url: str
    template_yaml_files: _containers.ScalarMap[str, str]
    values_yaml: str
    params: _containers.RepeatedCompositeFieldContainer[_param_pb2.InfraChartParam]
    web_links: InfraChartWebLinks
    def __init__(self, selector: _Optional[_Union[_selector_pb2.ApiResourceSelector, _Mapping]] = ..., description: _Optional[str] = ..., is_ready: bool = ..., icon_url: _Optional[str] = ..., template_yaml_files: _Optional[_Mapping[str, str]] = ..., values_yaml: _Optional[str] = ..., params: _Optional[_Iterable[_Union[_param_pb2.InfraChartParam, _Mapping]]] = ..., web_links: _Optional[_Union[InfraChartWebLinks, _Mapping]] = ...) -> None: ...

class InfraChartWebLinks(_message.Message):
    __slots__ = ("readme_raw_url", "chart_web_url")
    README_RAW_URL_FIELD_NUMBER: _ClassVar[int]
    CHART_WEB_URL_FIELD_NUMBER: _ClassVar[int]
    readme_raw_url: str
    chart_web_url: str
    def __init__(self, readme_raw_url: _Optional[str] = ..., chart_web_url: _Optional[str] = ...) -> None: ...
