# Minimum Time difference between two sendall calls for the recv method to count them as one -
# 0.000001
import socket
import threading
from sys import argv
from node import NetworkNode

HOST = socket.gethostbyname(socket.gethostname())


def send_messages_to_server(client_node: NetworkNode):
    client_node.send_message(NAME.encode())
    while True:
        message = input()
        if message == 'quit':
            break
        client_node.send_message(message.encode())


def receive_messages_from_server(client_node: NetworkNode):
    while True:
        message = client_node.recv_message()
        name = client_node.recv_message()
        print(f"{name}: {message}")


def run_client():
    """
    Driver function to connect to the server and send/recieve messages

    For communicating with the chat room, allowing receiving and sending of messages
    at the same time, a thread of `receive_messages_from_server` function is created for recieving
    the message which runs in the background, while the `send_messages_to_server` function is
    faclitates sending of messages to the server
    This setup allows to send and receive messages at the same time, receiver receiving message in
    the background while sender takes input messages and sends them to the server
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
    print("Type and press enter to send messages")

    if len(argv) == 1:
        NAME = input("Enter your name - ")
    else:
        NAME = argv[1]

    print()
    run_client()
