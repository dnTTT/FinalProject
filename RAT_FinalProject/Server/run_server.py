import socket
from Handler.database import Database


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def listen_to_computer_info():
    # Check socket types for report
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(b'Done')
                # Decode information received, and split by ||
                return data

def insert_on_database(collection, data):
    Database.new_connection(collection, data)

def create_object_for_database(hostname, ip_address, running_port, mac_address):
    object = {
        "Hostname": hostname,
        "Ip_address": ip_address,
        "Running_port": running_port,
        "Mac_address": mac_address
    }
    return object

if __name__ == '__main__':
    data = listen_to_computer_info()
    hostname, ip_address, running_port, mac_address = data.decode("Utf-8").split("||")

    Database.initialize()
    data_object = create_object_for_database(hostname, ip_address, running_port, mac_address)
    insert_on_database("Clients_Collection", data_object)


