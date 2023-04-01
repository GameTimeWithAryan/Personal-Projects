import socket
import threading
from secrets import compare_digest

from node import NetworkNode
from comms_protocol import MessageType, WRONG_PASSWORD_ERROR, report_wrong_packet, INVALID_MSG_LEN_ERROR, \
    WRONG_PACKET_MSG

# To broadcast the message to all clients and not exclude anyone
NO_CLIENT_ADDRESS = ("x.x.x.x", 0000)
# Server address
HOST, PORT = socket.gethostbyname(socket.gethostname()), 5050
# Connected/active clients list
clients: list[NetworkNode] = []


def authenticate_name(client_node: NetworkNode, username: str):
    """Checks username and authenticates if username is admin
    Returns None if username was not authenticated
    """
    log_msg: str = ""
    error_msg: str = ""

    # No auth required if user is not admin
    if username != "admin":
        return username

    # Receive a packet
    message_type, password = client_node.recv_message()

    # If the packet is not a PASSWORD type packet, then fill error_msg and log_msg
    if message_type != MessageType.PASSWORD.value:
        error_msg = WRONG_PACKET_MSG.format(listen=MessageType.PASSWORD.value, recv=message_type)
        log_msg = f"[{client_node.peer_address}] {error_msg}"

    # If the password is not correct, then fill error_msg and log_msg
    if not compare_digest(password, "adminpass"):
        error_msg = WRONG_PASSWORD_ERROR
        log_msg = f"[{client_node.peer_address}] {error_msg}"

    # If something was wrong, log_msg and error_msg would be reported
    if log_msg != "" and error_msg != "":
        report_wrong_packet(log_msg, error_msg, client_node)
        # return None if auth failed
        return None

    # If everything was correct then admin is authenticated
    client_node.send_message("Admin authenticated", MessageType.INFO)
    return username


def get_authenticated_name(client_node: NetworkNode, address: tuple[str, int]):
    # Keep listening for name until it is received and authenticated, or if an error occurs
    while True:
        try:
            # Receive a packet
            message_type, username = client_node.recv_message()

            # If the packet is not a NAME type packet, report it
            if message_type != MessageType.NAME.value:
                error_msg = WRONG_PACKET_MSG.format(listen="username", recv=message_type)
                log_msg = f"[{address}] {error_msg}"
                report_wrong_packet(log_msg, error_msg, client_node)
                continue

            # Check username and authenticate if necessary
            username = authenticate_name(client_node, username)
            # username is None if username did not get authorization
            # else username is authenticated
            if username is not None:
                return username

        except socket.error as e:
            clients.remove(client_node)
            print(e.strerror)
            return None
        except ValueError:
            report_wrong_packet(INVALID_MSG_LEN_ERROR, INVALID_MSG_LEN_ERROR, client_node)


def recieve_message(client_node: NetworkNode, username: str):
    # Keep listening for messages until it is received, or an error occurs
    while True:
        try:
            # Receive a packet
            message_type, chat_message = client_node.recv_message()

            if message_type == MessageType.MESSAGE.value:
                return chat_message

            # If not a message packet, inform client and log on console of wrong packet type
            error_msg = WRONG_PACKET_MSG.format(listen=MessageType.MESSAGE.value, recv=message_type)
            log_msg = f"[{username}] {error_msg}"
            report_wrong_packet(log_msg, error_msg, client_node)

        except socket.error:
            clients.remove(client_node)
            leave_message = f"{username} Left the chat"
            broadcast_message((client_node.peer_address,), None, leave_message, MessageType.INFO)
            print(f"[LEFT] {leave_message}")
            return None
        except ValueError:
            log_msg = f"[{username}] {INVALID_MSG_LEN_ERROR}"
            report_wrong_packet(log_msg, INVALID_MSG_LEN_ERROR, client_node)


def broadcast_message(exclude_addresses: tuple[tuple[str, int]], sender_name: str | None, message: str,
                      message_type: MessageType = MessageType.MESSAGE):
    """Send messages to all clients
    When sender_name is None, sends the message without sending username
    """

    # Iterate over all active client connections
    for c_node in clients.copy():
        try:
            # Don't broadcast if client in exclude addresses
            if c_node.peer_address in exclude_addresses:
                continue

            # If a sender_name is supplied, send the name first
            if sender_name:
                c_node.send_message(sender_name, MessageType.NAME)
            c_node.send_message(message, message_type)

        except socket.error:
            print(f"[BROADCAST ERROR] Error when sending to {c_node.peer_address}")
            clients.remove(c_node)
            print(f"[AUTOFIX] Removed {c_node.peer_address} from clients list")


def handle_client(connection: socket.socket, address: tuple[str, int]):
    client_node = NetworkNode(connection)
    clients.append(client_node)

    # Receive username
    username = get_authenticated_name(client_node, address)
    # If username is None, it means there was a socket.error caught
    if username is None:
        return
    print(f"[NAME] {address}: {username}")

    # Broadcasting join message
    join_message = f"{username} Entered the chat"
    # NO_CLIENT_ADDRESS is used to broadcast to all clients
    broadcast_message((NO_CLIENT_ADDRESS,), None, join_message, MessageType.INFO)

    # Listening for messages from client
    while True:
        message = recieve_message(client_node, username)
        # Message is None if a socket.error was caught
        if message is None:
            return
        # No need to broadcast empty messages
        if message == "":
            continue

        # Good message was received
        print(f"[MESSAGE] {username}: {message}")
        broadcast_message((address,), username, message)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SERVER:
    SERVER.bind((HOST, PORT))
    SERVER.listen()
    print(f"Listening on {HOST}:{PORT}\n")

    while True:
        client_socket, client_address = SERVER.accept()
        print(f"[CONNECTION] {client_address}")

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
