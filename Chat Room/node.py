"""
Protocol for communication:
For sending/receiving data, NetworkNode first sends/recieves message length
in a packet of size `HEADER` and then the actual message
"""

import socket
from enum import Enum, StrEnum, auto

HEADER = 5


class MessageType(StrEnum):
    INFO = auto()  # "{name} entered the chat" like messages
    MESSAGE = auto()  # Chat messages


class ErrorCode(Enum):
    INVALID_MSG_LEN = -1
    SOCKET_ERROR = -2


class NetworkNode:
    """A class for handling the sending and receiving of data over a network using sockets"""

    def __init__(self, connection: socket.socket):
        self.connection = connection

    def recv(self, size: int) -> str | tuple[None, ErrorCode]:
        """Receives an individual message packet"""
        try:
            return self.connection.recv(size).decode()
        except socket.error:
            return None, ErrorCode.SOCKET_ERROR

    def recv_message(self) -> str | tuple[None, ErrorCode]:
        """Receives complete message

        Following communication protocol, receives message length and packets
        until complete message of that length is received
        """

        message = ""
        try:
            message_length = int(self.recv(HEADER))  # May raise ValueError
            while len(message) < message_length:
                received_message = self.recv(message_length - len(message))
                message += received_message  # May raise Type error if received_message is None

        except ValueError:
            # received invalid message length
            return None, ErrorCode.INVALID_MSG_LEN
        except TypeError:
            # None was returned by self.recv, due to socket error
            return None, ErrorCode.SOCKET_ERROR

        return message

    def send(self, message: str):
        """Sends a single packet containing message"""
        self.connection.sendall(message.encode())

    def send_message(self, message: str):
        """Sends a message to the remote connection

        Following communication protocol,
        first sends the message length then the actual message
        """

        message_payload = self.make_send_payload(message)
        self.send(message_payload)

    @staticmethod
    def make_send_payload(message: str):
        """Adds message length header at start"""
        # length of bytes of message with padding to make it of size HEADER
        message_length = f'{len(message.encode()):<{HEADER}}'
        payload = message_length + message
        return payload
