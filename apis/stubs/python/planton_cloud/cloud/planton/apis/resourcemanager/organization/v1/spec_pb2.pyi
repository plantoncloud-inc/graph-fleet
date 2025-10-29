from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrganizationSpec(_message.Message):
    __slots__ = ("description", "logo_url", "stack_job_settings", "is_beta_features_enabled")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LOGO_URL_FIELD_NUMBER: _ClassVar[int]
    STACK_JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    IS_BETA_FEATURES_ENABLED_FIELD_NUMBER: _ClassVar[int]
    description: str
    logo_url: str
    stack_job_settings: OrganizationStackJobSettings
    is_beta_features_enabled: bool
    def __init__(self, description: _Optional[str] = ..., logo_url: _Optional[str] = ..., stack_job_settings: _Optional[_Union[OrganizationStackJobSettings, _Mapping]] = ..., is_beta_features_enabled: bool = ...) -> None: ...

class OrganizationStackJobSettings(_message.Message):
    __slots__ = ("is_default_stack_job_runner_disabled", "is_default_pulumi_backend_credential_disabled")
    IS_DEFAULT_STACK_JOB_RUNNER_DISABLED_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_PULUMI_BACKEND_CREDENTIAL_DISABLED_FIELD_NUMBER: _ClassVar[int]
    is_default_stack_job_runner_disabled: bool
    is_default_pulumi_backend_credential_disabled: bool
    def __init__(self, is_default_stack_job_runner_disabled: bool = ..., is_default_pulumi_backend_credential_disabled: bool = ...) -> None: ...
