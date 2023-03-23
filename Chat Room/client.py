import socket
import threading
from sys import argv

from node import NetworkNode
from comms_protocol import MessageType, WRONG_PASSWORD_ERROR, CONN_ERROR, INVALID_MSG_LEN_ERROR

HOST, PORT = socket.gethostbyname(socket.gethostname()), 5050
is_alive: bool = True


def get_username():
    # Pycharm IDE doesn't recognize global argv variable and gives warning
    if len(argv) == 2:
        username = argv[1]
        print(f"Enter your username - {username}")
    else:
        username = input("Enter your username - ")
    return username


def authenticate_with_server(client_node: NetworkNode):
    global is_alive
    while is_alive:
        try:
            username = get_username()

            # Sending username to server
            client_node.send_message(username, MessageType.NAME)
            # If username is not admin, no need for auth
            if username != "admin":
                break

            # Auth password for admin username
            password = input("Enter your password - ")
            client_node.send_message(password, MessageType.PASSWORD)

            _, response = client_node.recv_message()
            if response == WRONG_PASSWORD_ERROR:
                print("Wrong password")
                continue

            print("Authenticated as admin successfully\n")
            break
        except socket.error:
            print(CONN_ERROR)
            is_alive = False
            break


def send_messages_to_server(client_node: NetworkNode):
    global is_alive
    try:
        while is_alive:
            message = input()
            if message == "quit":
                is_alive = False
                break
            client_node.send_message(message, MessageType.MESSAGE)

    except socket.error:
        print(f"[SENDER] {CONN_ERROR}")
        return


def receive_messages_from_server(client_node: NetworkNode):
    received_message: str
    while is_alive:
        try:
            message_type, message = client_node.recv_message()
            match message_type:
                # Usually a join or a leave message of a client
                case MessageType.INFO.value:
                    received_message = f"{message}"
                case MessageType.NAME.value:
                    sender_name = message
                    # if username of sender is received, chat message should follow
                    _, chat_message = client_node.recv_message()
                    received_message = f"{sender_name}: {chat_message}"
                case no_matches:
                    print(f"Received invalid message type {no_matches}")
                    continue
            print(received_message)

        except socket.error:
            print(CONN_ERROR)
            break
        except ValueError:
            print(INVALID_MSG_LEN_ERROR)


def run_client():
    """
    For communicating with the chat room server, allowing receiving and sending of messages
    at the same time, a thread of `receive_messages_from_server` function is created,
    while the `send_messages_to_server` function faclitates sending of messages to the server
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # Try connecting to server
        try:
            client.connect((HOST, PORT))
        except socket.error:
            print("Cannot connect to server")
            print("Maybe the server is offline or you are not connected to the internet")

        client_node = NetworkNode(client)

        # First authenticate before starting sender and receiver functions
        authenticate_with_server(client_node)

        receiver_thread = threading.Thread(target=receive_messages_from_server, args=(client_node,))
        receiver_thread.start()

        send_messages_to_server(client_node)


if __name__ == "__main__":
    print("GWA's Chatroom")
    print("Type 'quit' to quit the program")
    print("Type and press enter to send message")
    print()
    run_client()
