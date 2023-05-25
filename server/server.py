import sys
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

def listenForClients(clientSet):
    # This function keeps listening for a message from the clientSet socket
    # Whenever a message is received, broadcast it to all other connected clients
    while True:
        try:
            # keep listening for a message from clientSet socket
            msg = clientSet.recv(1024).decode().strip() # Strip any leading/trailing whitespace
        except Exception as e:
            # if client is no longer connected, remove it from the set
            print(f"[!] Error: {e}")
            clientSocketList.remove(clientSet)
        else:
            if len(msg) <= 0:
                # if client disconnects, function returns empty message - quick and dirty fix
                raise Exception("Client disconnected!")
            if not msg:
                # ignore empty messages
                continue
            # performing basic input validation on received message
            if len(msg) > 255:
                # reject messages over 255 characters - good old SMS 
                print("[!] Error: Message too long. Ignoring")
                continue
            if not all(c.isprintable() for c in msg):
                # Reject messages containing non-printable characters
                print("[!] Error: Message contains non-printable characters. Ignoring")
                continue
            # if we received a message, replace the separator token with ":" for nice printing
            msg = msg.replace(sepToken, ":")
        # iterate over all connected sockets
        for clientSocket in clientSocketList:
            # and send the message
            clientSocket.send(msg.encode())

def monitorTerminationSignal():
    input("Press enter to stop the server\n")
    print("[*] Closing the server...")
    # close all client sockets
    for cs in clientSocketList:
        cs.close()
    # close server socket
    server.close()
    sys.exit(0)

terminaltionThread = Thread(target=monitorTerminationSignal)
terminaltionThread.start()

while True:
    # we keep listening for new connections all the time
    clientSocket, clientAddress = server.accept()
    print(f"[+] {clientAddress} connected.")
    # add the new connected client to connected sockets
    clientSocketList.add(clientSocket)
    # start a new thread that listens for each client's message
    thread = Thread(target=listenForClients, args=(clientSocket,))
    # make the thread daemon so is ends whenever the main thread ends
    thread.daemon = True
    # start the thread
    thread.start()