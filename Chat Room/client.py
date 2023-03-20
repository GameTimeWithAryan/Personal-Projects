import socket
import threading
from sys import argv

from node import NetworkNode, MessageType

HOST = socket.gethostbyname(socket.gethostname())
is_alive: bool = True


def send_messages_to_server(client_node: NetworkNode):
    global is_alive
    client_node.send_message(NAME)

    while True:
        message = input()
        if message == "quit":
            is_alive = False
            break
        try:
            client_node.send_message(message)
        except socket.error:
            print("Stopping send service")
            break


def receive_messages_from_server(client_node: NetworkNode):
    received_message: str
    while is_alive:
        try:
            message_type = client_node.recv_message()

            # Usually a join or a leave message of a client
            if message_type == MessageType.INFO.name:
                received_message = client_node.recv_message()
            # Chat Message of a client
            elif message_type == MessageType.MESSAGE.name:
                sender_name = client_node.recv_message()
                message = client_node.recv_message()
                received_message = f"{sender_name}: {message}"
            else:
                continue

            print(received_message)

        except socket.error:
            print("Network error")
            break
        except ValueError:
            print("Received invalid message length")


def run_client():
    """
    Main function to connect to the server and send/recieve messages

    For communicating with the chat room server, allowing receiving and sending of messages
    at the same time, a thread of `receive_messages_from_server` function is created,
    while the `send_messages_to_server` function faclitates sending of messages to the server
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, 5050))
        client_node = NetworkNode(client)

        receiver_thread = threading.Thread(target=receive_messages_from_server, args=(client_node,))
        receiver_thread.start()

        send_messages_to_server(client_node)


if __name__ == "__main__":
    print("GWA's Chatroom")
    print("Type 'quit' to quit the program")
    print("Type and press enter to send message")
    print()

    if len(argv) == 1:
        NAME = input("Enter your name - ")
    else:
        NAME = argv[1]
        print(f"Enter your name - {NAME}")

    run_client()
