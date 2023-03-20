from enum import StrEnum, auto


class MessageType(StrEnum):
    INFO = auto()  # "{name} entered the chat" messages
    MESSAGE = auto()  # Chat messages
