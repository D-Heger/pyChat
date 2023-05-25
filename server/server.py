import socket
from threading import Thread

# server ip settings
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # open port for server
seperator_token = "<SEP>" # this will be used to seperate client name & message

# initialize list/set all connected client's sockets
client_sockets = set()
# create a tcp socket
s = socket.socket()
# mark port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(20)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_clients(cs):
    """
    This function keeps listening for a message from the 'cs' socket
    Whenever a message is recived, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listeing for a message from 'cs' socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # if client no longer connected, remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we recive a message, replace the seperator token with ":" for nice printing
            msg = msg.replace(seperator_token, ":")
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())

while True:
    # we keep listening for new connections all the time
    client_socket, client_adress = s.accept()
    print(f"[+] {client_adress} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's message
    t = Thread(target=listen_for_clients, args=(client_socket,))
    # make the thread daemon so is ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close all client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()