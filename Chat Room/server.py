import socket
import threading
from secrets import compare_digest

from node import NetworkNode, MessageType, INVALID_MSG_LEN_ERROR, WRONG_PASSWORD_MSG, wrong_packet_msg

# to broadcast the message to all clients and not exclude anyone
NO_CLIENT_ADDRESS = ("x.x.x.x", 0000)
# server address
HOST, PORT = socket.gethostbyname(socket.gethostname()), 5050
# connected/active clients list
clients: list[NetworkNode] = []


def get_authenticated_name(client_node: NetworkNode, username: str):
    if username != "admin":
        return username

    message_type, password = client_node.recv_message()
    if message_type != MessageType.PASSWORD.value:
        log_msg = f"[{client_node.peer_address}] Listening for password packet, received {message_type}"
        send_msg = f"Listening for password packet, received {message_type}"
        wrong_packet_msg(log_msg, send_msg, client_node)
        return None
    if not compare_digest(password, "adminpass"):
        log_msg = f"[{client_node.peer_address}] Admin auth failed"
        wrong_packet_msg(log_msg, WRONG_PASSWORD_MSG, client_node)
        return None
    return username


def recieve_name(client_node: NetworkNode, address: tuple[str, int]):
    while True:
        try:
            message_type, username = client_node.recv_message()
            if message_type != MessageType.NAME.value:
                log_msg = f"[{address}] Listening for username packet, receievd {message_type}"
                send_msg = "Invalid request"
                wrong_packet_msg(log_msg, send_msg, client_node)
                continue

            username = get_authenticated_name(client_node, username)  # username of sender
            if username is not None:
                return username

        except socket.error as e:
            clients.remove(client_node)
            print(e.strerror)
            return None
        except ValueError:
            wrong_packet_msg(INVALID_MSG_LEN_ERROR, INVALID_MSG_LEN_ERROR, client_node)


def recieve_message(client_node: NetworkNode, username):
    while True:
        try:
            message_type, chat_message = client_node.recv_message()
            if message_type == MessageType.MESSAGE.value:
                return chat_message
            print(f"[{client_node.peer_address}] Listening for msg packet, received {message_type}")

        except socket.error:
            clients.remove(client_node)
            leave_message = f"{username} Left the chat"
            broadcast_message((client_node.peer_address,), None, leave_message, MessageType.INFO)
            print(f"[CLOSED] {username}")
            return None
        except ValueError:
            wrong_packet_msg(INVALID_MSG_LEN_ERROR, INVALID_MSG_LEN_ERROR, client_node)


def broadcast_message(exlcue_addresses: tuple[tuple[str, int]], sender_name: str | None, message: str,
                      message_type: MessageType = MessageType.MESSAGE):
    """Send messages to all clients, when sender_name is None, sends the message without sending username"""

    for c_node in clients.copy():
        try:
            if c_node.peer_address in exlcue_addresses:
                continue

            # Broadcast if not client is not an excluded address
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

    # Listening for username
    username = recieve_name(client_node, address)
    if username is None:
        return
    print(f"[NAME] {address}: {username}")

    # Broadcasting join message
    join_message = f"{username} Entered the chat"
    broadcast_message((NO_CLIENT_ADDRESS,), None, join_message, MessageType.INFO)

    # Listening for messages
    while True:
        message = recieve_message(client_node, username)
        if message is None:
            return
        if message == "":
            continue

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
