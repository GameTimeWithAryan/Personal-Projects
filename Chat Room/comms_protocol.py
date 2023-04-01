from enum import StrEnum

# Header size constants
MSG_LEN_HEADER_SIZE = 5
MSG_TYPE_HEADER_SIZE = 10
HEADER_SIZE = MSG_LEN_HEADER_SIZE + MSG_TYPE_HEADER_SIZE

# Error messages
CONN_ERROR = "Connection Broken"
INVALID_MSG_LEN_ERROR = "Invlaid message length received"
WRONG_PASSWORD_ERROR = "WRONG_PASSWORD"

# listen = listening type, recv = received type
WRONG_PACKET_MSG = "Expected {listen} packet, but received {recv} packet"


class MessageType(StrEnum):
    """Enum for message types of Header"""
    INFO = "INFO"  # "{name} entered the chat" like messages, info messages
    NAME = "NAME"  # for sharing names of clients between server and client
    MESSAGE = "MESSAGE"  # chat messages
    PASSWORD = "PASSWORD"  # message containing the password for admin auth


# NetworkNode string for type hinting
NetworkNode = 'NetworkNode'


def report_wrong_packet(log_msg: str, send_msg: str, client_node: NetworkNode):
    """Logs log_msg to console and sends the send_msg to client
    To be called when a wrong type of packet is receievd
    """

    print(log_msg)
    client_node.send_message(send_msg, MessageType.INFO)
