"""
Protocol for communication:
For sending/receiving data, NetworkNode first sends/recieves message length
in a packet of size `HEADER` and then the actual message
"""

import socket
from enum import StrEnum, auto

HEADER = 5
CONN_ERROR_MSG = "Connection Broken"
INVALID_MSG_LEN_ERROR_MSG = "Invlaid message length received"


class MessageType(StrEnum):
    INFO = auto()  # "{name} entered the chat" like messages, info messages
    MESSAGE = auto()  # Chat messages


class NetworkNode:
    """A class for handling the sending and receiving of data over a network using sockets"""

    def __init__(self, connection: socket.socket):
        self.connection = connection

    def recv(self, size: int) -> str:
        """Receives an individual message packet"""
        return self.connection.recv(size).decode()

    def recv_message(self) -> str:
        """Receives complete message

        Following communication protocol, receives message length and packets
        until complete message of that length is received

        Raises
        ------
        ValueError - On invalid msg length
        """

        message = ""
        # Receive message header, and listen for packets according to length in header
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

        message_packet = self.add_header(message)
        self.send(message_packet)

    @staticmethod
    def add_header(message: str):
        """Adds message length header to message for sending"""
        # length of "bytes of message" with padding to make its length equal to `HEADER`
        message_length = f'{len(message.encode()):<{HEADER}}'
        message_packet = message_length + message
        return message_packet
