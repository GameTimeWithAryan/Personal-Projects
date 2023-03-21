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
When a client connnects to the server, the server starts listening for message packets of
type `NAME`, this will be the name of the client to be displayed in the chatroom

After receiving name, the server starts listening for message packets of `MSG`

On receviving the message, the server broadcasts it to all other connected client
except the sender

### Client
When a client connects to the server, it sends its name to the server

After that, it becomes ready to send chat messages