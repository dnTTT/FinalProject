import socket
from time import sleep

# configure socket and connect to server
clientSocket = socket.socket()
host = socket.gethostname()
port = 25000
clientSocket.connect((host, port))

# keep track of connection status
connected = True
print("connected to server")

while True:
    # attempt to send and receive wave, otherwise reconnect
    try:
        message = clientSocket.recv(1024).decode("UTF-8")
        clientSocket.send(bytes("Client wave", "UTF-8"))
        print(message)
    except socket.error:
        # set connection status and recreate socket
        connected = False
        clientSocket = socket.socket()
        print("connection lost... reconnecting")
        while not connected:
            # attempt to reconnect, otherwise sleep for 2 seconds
            try:
                clientSocket.connect((host, port))
                connected = True
                print("re-connection successful")
            except socket.error:
                sleep(2)

clientSocket.close();  