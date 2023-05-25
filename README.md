## pyChat - Simple console-based chat application made with python<br>
pyChat is a console-based chat application, using pythons built in socket module.
Currently, it doesn't offer many features but can be easily expanded or reworked to fit your specific needs.

### Built with
[![Python][python]][python-url]

### Usage
If you want to run this application locally, you don't have to change any code.
If you want to run this application online (which in the current state I wouldn't recommend, as it's insecure), you need to change the **SERVER_HOST and SERVER_PORT** values in **both server.py and client.py** to your local/server's IP and a port of your choice. Just make sure that the port you want to use is open.

### Features
The current feature set includes:
#### Server
- Server opens a socket and waits for clients to connect
- If connected, Server prints a log which user connected and adds them to a list of Clients
- Server listens for new messages from Client in separate threads
- If a new message is received by the Server, send it to all Clients connected
- If connection breaks with a Client, remove Client from the list
- (Currently, Server offers no Chat Logs - You need to connect as Client to read)
#### Client
- After starting Client application, it automatically tries to connect with Server
- Client is informed what server they are connecting to and if the connection was successful
- Client gets assigned a random color and is asked to input a name
- Now Client can send messages, which will be broadcast to all other connected Clients
- With /exit as message, the Client can safely disconnect from the Server.. This is broadcast to other Clients, informing them about the disconnect. 
- With /rename as message, Client is able to change their username. This is broadcast to other Clients, informing them about the name change.


### Many thanks to
Abdou Rockikz and thepythoncode.com for inspiring me to create this chat application as well as setting up the basic server/client code with the help of their tutorial!

<!-- Links and Images -->
[python]:https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]:https://www.python.org/
