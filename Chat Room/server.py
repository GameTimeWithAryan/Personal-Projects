import socket
import threading
from node import NetworkNode

clients: list[NetworkNode] = []

HOST, PORT = socket.gethostbyname(socket.gethostname()), 5050
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


def handle_client(client_node: NetworkNode, address: str):
    """Recieves message from a client and broadcasts
    it to all other clients connected to server

    Parameters
    ----------
    client_node : NetworkNode
        NetworkNode to be used for sending and receiving data
    address : str
        address of socket
    """

    print(f"[CONNECTION] {address}")
    name = client_node.recv_message()
    print(f"{name} Entered the chat")

    while True:
        try:
            message = client_node.recv_message()

            print(f"[MESSAGE] {name}: {message}")
            for c_node in clients:
                if c_node.connection.getpeername() != client_node.connection.getpeername():
                    c_node.send_message(message.encode())
                    c_node.send_message(name.encode())

        # ConnectionAbortedError or similar errors might be raised when a client disconnects
        # and the server still tries to do operations on the client socket
        except socket.error:
            print(f"[{name}] Connection Broken")
            clients.remove(client_node)
            client_node.connection.close()
            break


def run_server():
    server.listen()
    print(f"Listening on {HOST}\n")
    while True:
        client_socket, client_address = server.accept()

        client_node = NetworkNode(client_socket)
        clients.append(client_node)

        thread = threading.Thread(target=handle_client, args=(client_node, client_address))
        thread.start()


if __name__ == "__main__":
    run_server()
