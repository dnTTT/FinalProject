import socket
from Handler.database import Database
from PyQt5 import QtWidgets, uic
import sys
from UI.Main import MainWindow

HOST = "192.168.0.129"  # Standard loopback interface address (localhost)
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

def create_object_for_database(hostname, ip_address, running_port, mac_address, width, height):
    object = {
        "Hostname": hostname,
        "Ip_address": ip_address,
        "Running_port": running_port,
        "Mac_address": mac_address,
        "Width": width,
        "Height": height
    }
    return object

if __name__ == '__main__':
    data = listen_to_computer_info()
    hostname, ip_address, running_port, mac_address, width, height = data.decode("Utf-8").split("||")

    Database.initialize()
    data_object = create_object_for_database(hostname, ip_address, running_port, mac_address, width, height)
    insert_on_database("Clients_Collection", data_object)

    app = QtWidgets.QApplication(sys.argv)
    populate_list_data = Database.get_all("Clients_Collection")
    data_list = []
    for x in populate_list_data:
        data_list.append(x)

    window = MainWindow()

    window.load_data_to_table(data_list)
    app.exec_()


