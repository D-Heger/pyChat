import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# initialize colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]

# choose a random color for the client
clientColor = random.choice(colors)

# server's IP address - if the server is not on this machine, put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
sepToken = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
server = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
server.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# print out possible user commands and other relevant information
print("[?] Max length of message is 255 characters.")
print("[?] Type '/exit' as your message to exit the chat.")
print("[?] Type '/rename' as your message to change your name.")

# prompt the client for a name
username = input("Enter your name: ")

def listenForMessages():
    while True:
        message = server.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
thread = Thread(target=listenForMessages)
# make the thread daemon so it ends whenever the main thread ends
thread.daemon = True
# start the thread
thread.start()

while True:
    # input message we want to send to the server
    toSend =  input()
    # a way to exit the program
    if toSend == "/exit":
        toSend = f"{clientColor}[{dateNow}] {username} has left the conversation"
        server.send(toSend.encode())
        break
    # a way for users to rename themselves
    if toSend == "/rename":
        newname = input("Enter your new name: ")
        toSend = f"{clientColor} {username} has changed their name to {newname}"
        username = newname
    # add the datetime, name & the color of the sender
    dateNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    toSend = f"{clientColor}[{dateNow}] {username}{sepToken}{toSend}{Fore.RESET}"
    # finally, send the message
    server.send(toSend.encode())

# close the socket
server.close()