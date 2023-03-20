"""
Protocol for communication:
For sending/receiving data, NetworkNode first sends/recieves message length
in a packet of size `HEADER` and then the actual message
"""

import socket
from enum import StrEnum, auto

HEADER = 5


class MessageType(StrEnum):
    INFO = auto()  # "{name} entered the chat" like messages, info messages
    MESSAGE = auto()  # Chat messages


class NetworkNode:
    """A class for handling the sending and receiving of data over a network using sockets"""

    def __init__(self, connection: socket.socket):
        self.connection = connection

    def recv(self, size: int) -> str:
        """Receives an individual message packet
        Raises - socket.error if Connection error is there"""

        return self.connection.recv(size).decode()

    def recv_message(self) -> str:
        """Receives complete message

        Following communication protocol, receives message length and packets
        until complete message of that length is received

        Raises
        ------
        socket.error - Connection error
        ValueError - On invalid msg length
        """

        message = ""
        message_length = int(self.recv(HEADER))  # May raise ValueError
        while len(message) < message_length:
            received_message = self.recv(message_length - len(message))
            message += received_message

        return message

    def send(self, message: str):
        """Sends a single packet containing message"""
        self.connection.sendall(message.encode())

    def send_message(self, message: str):
        """Sends a message to the remote connection

        Following communication protocol,
        sends a packet containing HEADER and message body
        """

        message_payload = self.make_send_protocol_payload(message)
        self.send(message_payload)

    @staticmethod
    def make_send_protocol_payload(message: str):
        """Adds message length header at start"""
        # length of "bytes of message" with padding to make it of size HEADER
        message_length = f'{len(message.encode()):<{HEADER}}'
        payload = message_length + message
        return payload
