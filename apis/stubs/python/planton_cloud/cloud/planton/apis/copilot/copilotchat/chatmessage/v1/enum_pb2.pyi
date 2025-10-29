from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    chat_message_type_unknown: _ClassVar[ChatMessageType]
    bot: _ClassVar[ChatMessageType]
    system: _ClassVar[ChatMessageType]
    human: _ClassVar[ChatMessageType]

class ChatMessageUserAgentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    chat_message_user_agent_type_unknown: _ClassVar[ChatMessageUserAgentType]
    web_console: _ClassVar[ChatMessageUserAgentType]
    cli_terminal: _ClassVar[ChatMessageUserAgentType]
chat_message_type_unknown: ChatMessageType
bot: ChatMessageType
system: ChatMessageType
human: ChatMessageType
chat_message_user_agent_type_unknown: ChatMessageUserAgentType
web_console: ChatMessageUserAgentType
cli_terminal: ChatMessageUserAgentType
