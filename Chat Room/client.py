import socket
import threading
from sys import argv

from node import NetworkNode, MessageType, CONN_ERROR_MSG, INVALID_MSG_LEN_ERROR_MSG

HOST, PORT = socket.gethostbyname(socket.gethostname()), 5050
is_alive: bool = True


def send_messages_to_server(client_node: NetworkNode):
    global is_alive
    try:
        client_node.send_message(NAME, MessageType.NAME)

        while True:
            message = input()
            if message == "quit":
                is_alive = False
                break
            client_node.send_message(message, MessageType.MSG)
    except socket.error:
        print(CONN_ERROR_MSG)
        print("Stopping send service")
        return


def receive_messages_from_server(client_node: NetworkNode):
    received_message: str
    while is_alive:
        try:
            message_type, message = client_node.recv_message()

            # Usually a join or a leave message of a client
            if message_type == MessageType.INFO.value:
                received_message = message
            elif message_type == MessageType.NAME.value:
                sender_name = message
                # if name of sender is received, chat message should follow
                _, chat_message = client_node.recv_message()
                received_message = f"{sender_name}: {chat_message}"
            else:
                print("Invalid message type, trying again")
                continue

            print(received_message)

        except socket.error:
            print(CONN_ERROR_MSG)
            break
        except ValueError:
            print(INVALID_MSG_LEN_ERROR_MSG)


def run_client():
    """
    For communicating with the chat room server, allowing receiving and sending of messages
    at the same time, a thread of `receive_messages_from_server` function is created,
    while the `send_messages_to_server` function faclitates sending of messages to the server
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
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
