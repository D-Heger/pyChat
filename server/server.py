import socket
from threading import Thread

# server IP settings
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # open port for server
sepToken = "<SEP>" # this will be used to separate client name & message

# initialize list/set all connected client's sockets
clientSocketList = set()
# create a TCP socket
server = socket.socket()
# mark port as reusable port
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
server.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
server.listen(20)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_clients(cs):
    """
    This function keeps listening for a message from the 'CS' socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from 'CS' socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # if client no longer connected, remove it from the set
            print(f"[!] Error: {e}")
            clientSocketList.remove(cs)
        else:
            # if we received a message, replace the separator token with ":" for nice printing
            msg = msg.replace(sepToken, ":")
        # iterate over all connected sockets
        for clientSocket in clientSocketList:
            # and send the message
            clientSocket.send(msg.encode())

while True:
    # we keep listening for new connections all the time
    clientSocket, clientAddress = server.accept()
    print(f"[+] {clientAddress} connected.")
    # add the new connected client to connected sockets
    clientSocketList.add(clientSocket)
    # start a new thread that listens for each client's message
    thread = Thread(target=listen_for_clients, args=(clientSocket,))
    # make the thread daemon so is ends whenever the main thread ends
    thread.daemon = True
    # start the thread
    thread.start()


# close all client sockets
for cs in clientSocketList:
    cs.close()
# close server socket
server.close()