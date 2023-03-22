# GWA's Chat Room

This is a chatroom implmented using tcp sockets, it is not secure

## Protocol
### Node
Each node can communicate (send/recieve messages) by sending message packets.
Each message packet contains a Header and message body

First 5 bytes of the header contains length of the message body

Next 10 bytes contain the message type

Rest is the message body

### Server
When a client connnects to the server, the server starts listening for `NAME` packets,
this will be the username of the client to be displayed in the chatroom

If the username is admin, then the server listens for `PASSWORD` packets containing password
of admin for authentication

After that, the server listens for `MSG` packets

On receviving the chat messages, the server broadcasts it to all other connected client
except the sender

### Client
When a client connects to the server, it sends its username to the server

If the username is admin, then it also sends a password entered by client to server for auth

After that, it becomes ready to send chat messages