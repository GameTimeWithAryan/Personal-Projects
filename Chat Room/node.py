"""
Protocol for communication:
For sending/receiving data, NetworkNode first sends/recieves message length
in a packet of size `HEADER_SIZE` and then the actual message
"""
import socket
from comms_protocol import MessageType, MSG_LEN_HEADER_SIZE, MSG_TYPE_HEADER_SIZE


class NetworkNode:
    """A class for handling the sending and receiving of data over a network using sockets
    All methods execpt property peer_address raise socket.error if any socket error occours
    """

    def __init__(self, connection: socket.socket):
        self.connection = connection

    @property
    def peer_address(self):
        try:
            return self.connection.getpeername()
        except OSError:
            return None

    def recv(self, size: int) -> str:
        """Receives an individual message packet"""
        return self.connection.recv(size).decode()

    def recv_message(self) -> tuple[str, str]:
        """Receives complete message packets, returns message type and message

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
        message_type = self.recv(MSG_TYPE_HEADER_SIZE)
        # Receive message body
        while len(message) < message_length:
            received_message = self.recv(message_length - len(message))
            message += received_message

        return message_type.strip(), message.strip()

    def send(self, message: str):
        """Sends a single packet containing message"""
        self.connection.sendall(message.encode())

    def send_message(self, message: str, message_type: MessageType):
        """Sends a message to the remote connection
        Adds Header to message before sending

        Following communication protocol,
        sends a packet containing header and message body
        """

        message_packet = self.add_header(message, message_type.value)
        self.send(message_packet)

    @staticmethod
    def add_header(message: str, message_type: str):
        """Adds message length and message type headers to message for sending"""
        # length of "bytes of message" with padding to make its length equal to `MSG_LEN_HEADER_SIZE`
        message_length = f"{len(message.encode()):<{MSG_LEN_HEADER_SIZE}}"
        message_type = f"{message_type:<{MSG_TYPE_HEADER_SIZE}}"
        message_packet = message_length + message_type + message
        return message_packet
