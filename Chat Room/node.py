"""
Protocol for communication:
For sending/receiving data, NetworkNode first sends/recieves message length
of size `MSG_LEN_HEADER_SIZE` and then message type and then message email_body
"""
import socket
from comms_protocol import MessageType, MSG_LEN_HEADER_SIZE, MSG_TYPE_HEADER_SIZE


class NetworkNode:
    """A class for handling the sending and receiving of data over a network using sockets
    All methods execpt property peer_address raise socket.error if any connection error occurs
    """

    def __init__(self, connection: socket.socket):
        self.connection = connection

    @property
    def peer_address(self):
        try:
            # Get remote/receiver address
            return self.connection.getpeername()
        except OSError:
            return None

    def recv(self, size: int) -> str:
        """Receieve data of size `size`"""
        return self.connection.recv(size).decode()

    def recv_message(self) -> tuple[str, str]:
        """Receives complete message packets, returns message type and message email_body

        Following communication protocol, receives message length, message type and message email_body
        until complete message email_body of that length is received

        Raises
        ------
        ValueError - On invalid msg length
        """

        message_body = ""
        # Receive message length header, and listen for data accordingly
        message_length = int(self.recv(MSG_LEN_HEADER_SIZE))  # May raise ValueError
        # Receive message type header
        message_type = self.recv(MSG_TYPE_HEADER_SIZE)
        # Receive message body according to message length
        while len(message_body) < message_length:
            received_message = self.recv(message_length - len(message_body))
            message_body += received_message

        return message_type.strip(), message_body.strip()

    def send(self, data: str):
        """Sends data"""
        self.connection.sendall(data.encode())

    def send_message(self, message_body: str, message_type: MessageType):
        """Sends a message to the remote connection
        Adds header to message before sending

        Following communication protocol,
        sends a packet containing header and message email_body
        """

        message_packet = self.add_header(message_body, message_type.value)
        self.send(message_packet)

    @staticmethod
    def add_header(message_body: str, message_type: str) -> str:
        """Adds message length and message type headers to message email_body
        To prepare for sending message following the protocol
        """

        # message length header will be number of bytes objects the message occupies
        # Add padding to the string of len(message.encode()) to make its length equal to `MSG_LEN_HEADER_SIZE`
        message_length = f"{len(message_body.encode()):<{MSG_LEN_HEADER_SIZE}}"
        message_type = f"{message_type:<{MSG_TYPE_HEADER_SIZE}}"
        message_packet = message_length + message_type + message_body
        return message_packet
