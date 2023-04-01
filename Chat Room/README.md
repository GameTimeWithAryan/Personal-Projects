# GWA's Chat Room

This is a chatroom implmented using tcp sockets, but it is not secure

## Application Layer Protocol
### Node
Each node can communicate (send/recieve messages) using message packets.
Each message packet contains a **Header** and **Message body**

First 5 bytes of the header contains *length of the message body*

Next 10 bytes contain the *message type*

Rest is the *message body*

### Server
When a client connnects to the server, the server starts listening for `NAME` packets,
this will be the username of the client to be displayed in the chatroom

If the username is admin, then the server listens for `PASSWORD` packets containing
password of admin for authentication

After successful authentication, the server listens for `MSG` packets

On receviving a `MSG` packet, the server broadcasts the message to all other connected
clients except the sender

If the server received a packet of the type it was not listening for, it would
send the client a message about an invalid packet. It would also log it to the console.

### Client
When a client connects to the server, it sends its username to the server

If the username is admin, then it also sends a password entered by client to server for auth

After that, it becomes ready to send chat messages