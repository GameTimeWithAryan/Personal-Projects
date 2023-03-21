"""
Protocol for communication:
For sending/receiving data, NetworkNode first sends/recieves message length
in a packet of size `HEADER_SIZE` and then the actual message
"""

import socket
from enum import StrEnum

MSG_LEN_HEADER_SIZE = 5
MSG_TYPE_HEADER_SIZE = 10
HEADER_SIZE = MSG_LEN_HEADER_SIZE + MSG_TYPE_HEADER_SIZE
CONN_ERROR = "Connection Broken"
INVALID_MSG_LEN_ERROR = "Invlaid message length received"


class MessageType(StrEnum):
    INFO = "INFO"  # "{name} entered the chat" like messages, info messages
    NAME = "NAME"  # for sharing names of clients between server and client
    MSG = "MSG"  # chat messages


class NetworkNode:
    """A class for handling the sending and receiving of data over a network using sockets"""

    def __init__(self, connection: socket.socket):
        self.connection = connection

    def recv(self, size: int) -> str:
        """Receives an individual message packet"""
        return self.connection.recv(size).decode()

    def recv_message(self) -> tuple[str, str]:
        """Receives complete message with message type

        Following communication protocol, receives message length and packets
        until complete message of that length is received

        Raises
        ------
        ValueError - On invalid msg length
        """

        message = ""
        # Receive message length header, and listen for packets according to length in header
        message_length = int(self.recv(MSG_LEN_HEADER_SIZE))  # May raise ValueError
        # Receive message type header
        message_type = self.recv(MSG_TYPE_HEADER_SIZE).strip()
        # Receive message body
        while len(message) < message_length:
            received_message = self.recv(message_length - len(message))
            message += received_message

        return message_type, message

    def send(self, message: str):
        """Sends a single packet containing message"""
        self.connection.sendall(message.encode())

    def send_message(self, message: str, message_type: MessageType):
        """Sends a message to the remote connection

        Following communication protocol,
        sends a packet containing header and message body
        """

        message_packet = self.add_header(message, message_type.value)
        self.send(message_packet)

    @staticmethod
    def add_header(message: str, message_type: str):
        """Adds message length and message type headers to message for sending"""
        # length of "bytes of message" with padding to make its length equal to `HEADER_SIZE`
        message_length = f"{len(message.encode()):<{MSG_LEN_HEADER_SIZE}}"
        message_type = f"{message_type:<{MSG_TYPE_HEADER_SIZE}}"
        message_packet = message_length + message_type + message
        return message_packet

    @staticmethod
    def interpret_message(message_packet: str):
        message_length = message_packet[:MSG_LEN_HEADER_SIZE].strip()
        message_type = message_packet[MSG_LEN_HEADER_SIZE:MSG_TYPE_HEADER_SIZE].strip()
        message = message_packet[MSG_TYPE_HEADER_SIZE:]
        return message_length, message_type, message
