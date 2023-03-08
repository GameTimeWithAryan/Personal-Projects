"""
A message is a decoded packet received from a TCP socket

Protocol for communication:
For sending/receiving data, NetworkNode first sends/recieves message length
in a packet of size `HEADER` and then the actual message
"""

import socket
import sys

HEADER = 5


class NetworkNode:
    """A class for handling the sending and receiving of data over a network using sockets

    Attributes
    ----------
    connection : socket.socket
        Socket to receive and send data to
    """
    def __init__(self, connection: socket.socket):
        self.connection = connection

    def recv(self, size: int) -> str:
        """Receives an individual message

        Parameters
        ----------
        size : int
            size of packet to receive

        Returns
        -------
        str
            decoded rceived string meessage
        """
        try:
            return self.connection.recv(size).decode()
        except socket.error:
            print("Connection Closed")
            sys.exit()

    def recv_message(self) -> str | None:
        """Receives complete message

        Following communication protocol, receives message length and packets
        until complete message of that length is received

        Returns
        -------
        message : str or None
            decoded received complete string message
            Or returns None if invalid message length is received
        """

        message = ""

        try:
            message_length = int(self.recv(HEADER))
        except ValueError:
            print("Received invalid message length")
            return None

        while len(message) < message_length:
            received_message = self.recv(message_length - len(message))
            message += received_message
        return message

    def send(self, message: bytes):
        """Sends a single packet containing message

        Parameters
        ----------
        message : str
            bytes object to send
        """

        self.connection.sendall(message)

    def send_message(self, message: bytes):
        """Sends a message to the server

        Following communication protocol,
        first sends the message length then the actual message
        """
        message_length = f'{len(message):<{HEADER}}'.encode()
        self.send(message_length)
        self.send(message)
