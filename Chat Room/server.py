import socket
import threading

from node import NetworkNode, MessageType, CONN_ERROR, INVALID_MSG_LEN_ERROR

# It can be used in broadcast_message function to indicate
# the intent to broadcast the message to all clients and not exclude anyone
NO_CLIENT_ADDRESS = ("x.x.x.x", 0000)
HOST, PORT = socket.gethostbyname(socket.gethostname()), 5050
clients: list[NetworkNode] = []


def recieve_name(client_node: NetworkNode, address: tuple[str, int]):
    while True:
        try:
            message_type, message = client_node.recv_message()
            if message_type == MessageType.NAME.value:
                return message  # Name of sender
            print(f"[{address}] Listening for name packet, receievd {message_type}")
        except socket.error as e:
            clients.remove(client_node)
            print(e.strerror)
            return None
        except ValueError:
            print(INVALID_MSG_LEN_ERROR)


def recieve_message(client_node: NetworkNode, address, name):
    while True:
        try:
            message_type, message = client_node.recv_message()
            if message_type == MessageType.MSG.name:
                return message
            print(f"[{address}] Listening for msg packet, received {message_type}")
        except socket.error:
            clients.remove(client_node)
            leave_message = f"{name} Left the chat"
            broadcast_message(address, None, leave_message, MessageType.INFO)
            print(f"[CLOSED] {name}")
            return None
        except ValueError:
            print(INVALID_MSG_LEN_ERROR)


def broadcast_message(exlcue_address: tuple[str, int], sender_name: str | None, message: str,
                      message_type: MessageType = MessageType.MSG):
    """Send messages to all clients, when sender_name is None, sends the message without sending name"""

    for c_node in clients.copy():
        try:
            if c_node.connection.getpeername() != exlcue_address:
                if sender_name:
                    c_node.send_message(sender_name, MessageType.NAME)
                c_node.send_message(message, message_type)
        except socket.error:
            print(f"[BROADCAST ERROR] Error when sending to {c_node.connection.getpeername()}")
            clients.remove(c_node)
            print(f"[AUTOFIX] Removed {c_node.connection.getpeername()} from clients list")


def handle_client(connection: socket.socket, address: tuple[str, int]):
    client_node = NetworkNode(connection)
    clients.append(client_node)

    # Listening for name
    name = recieve_name(client_node, address)
    if name is None:
        return
    print(f"[NAME] {address}: {name}")

    # Broadcasting join message
    join_message = f"{name} Entered the chat"
    broadcast_message(NO_CLIENT_ADDRESS, None, join_message, MessageType.INFO)

    # Listening for messages
    while True:
        message = recieve_message(client_node, address, name)
        if message is None:
            return
        print(f"[MESSAGE] {name}: {message}")
        broadcast_message(address, name, message)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SERVER:
    SERVER.bind((HOST, PORT))
    SERVER.listen()
    print(f"Listening on {HOST}:{PORT}\n")

    while True:
        client_socket, client_address = SERVER.accept()
        print(f"[CONNECTION] {client_address}")

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
