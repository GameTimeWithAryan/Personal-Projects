import socket
import threading

from node import NetworkNode, MessageType

# It can be used in broadcast_message function to indicate
# the intent to broadcast the message to all clients and not exclude anyone
NO_CLIENT_ADDRESS = ("x.x.x.x", 0000)
HOST, PORT = socket.gethostbyname(socket.gethostname()), 5050
clients: list[NetworkNode] = []


def broadcast_message(exlcue_address: tuple[str, int], sender_name: str | None, message: str,
                      message_type: str = MessageType.MESSAGE.name):
    """Send messages to all clients, when sender_name is None, sends the message, without sending name"""
    for c_node in clients:
        if c_node.connection.getpeername() != exlcue_address:
            c_node.send_message(message_type)
            if sender_name:
                c_node.send_message(sender_name)
            c_node.send_message(message)


def handle_client(connection: socket.socket, address: tuple[str, int]):
    client_node = NetworkNode(connection)
    clients.append(client_node)

    while True:
        try:
            name = client_node.recv_message()
            break
        except socket.error:
            print("Connection broken")
            return
        except ValueError:
            print("Received invalid message length")
            client_node.send_message("INVALID_MESSAGE_LENGTH")

    print(f"[NAME] {address}: {name}")

    join_message = f"{name} Entered the chat"
    broadcast_message(NO_CLIENT_ADDRESS, None, join_message, MessageType.INFO.name)

    while True:
        try:
            message = client_node.recv_message()
        except socket.error:
            clients.remove(client_node)
            leave_message = f"{name} Left the chat"
            broadcast_message(address, None, leave_message, MessageType.INFO.name)
            break
        except ValueError:
            continue

        print(f"[MESSAGE] {name}: {message}")
        broadcast_message(address, name, message)

    print(f"[CLOSED] {name}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SERVER:
    SERVER.bind((HOST, PORT))
    SERVER.listen()
    print(f"Listening on {HOST}:{PORT}\n")

    while True:
        client_socket, client_address = SERVER.accept()
        print(f"[CONNECTION] {client_address}")

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()