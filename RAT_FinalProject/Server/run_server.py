import socket

import win32api

from Handler.database import Database
from PyQt5 import QtWidgets, uic
import sys
from UI.Main import MainWindow
import threading
from contextlib import closing
import ssl

HOST = "192.168.2.72"
PORT = 65432

def listen_to_computer_info():
    # SSLContext.wrap not working because hostname mismatch (on dynamic local ip), update later with a web server
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #context.load_cert_chain('../certificates2/server.crt', '../certificates2/server.key')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))

        try:
            sock.listen(5)
            print('Server started.')

            while 'connected':
                #with context.wrap_socket(sock, server_side=True) as ssock:
                client_sock, client_address = sock.accept()
                ssl_client_sock = ssl.wrap_socket(client_sock,
                                                  server_side=True,
                                                  certfile="../certificates2/server.crt",
                                                  keyfile="../certificates2/server.key")

                #client_sock, addr = sock.accept()

                data = ssl_client_sock.recv(1024)
                # client_sock.sendall(b'Done')
                win32api.MessageBox(0, f'New client connected: {client_address}', 'New client')
                if len(data) > 0:
                    # Decode information received, and split by ||
                    ip_address, running_port, mac_address, width, height = data.decode("Utf-8").split("||")
                    data_object = create_object_for_database(ip_address, running_port, mac_address, width,
                                                             height, "Active")
                    insert_on_database("Clients_Collection", data_object)
                    find_active_devices_thread = threading.Thread(target=find_active_devices)
                    find_active_devices_thread.start()
                    update_on_new_connection()


        finally:
            client_sock.close()

def get_all_clients():
    return Database.get_all("Clients_Collection")


def update_on_new_connection():
    populate_list_data = get_all_clients()
    data_list = []
    for x in populate_list_data:
        data_list.append(x)
    window.load_data_to_table(data_list)


def insert_on_database(collection, data):
    Database.new_update_connection(collection, data)


def create_object_for_database(ip_address, running_port, mac_address, width, height, status):
    object = {
        "Ip_address": ip_address,
        "Running_port": running_port,
        "Mac_address": mac_address,
        "Width": width,
        "Height": height,
        "Status": status
    }
    return object


def find_active_devices():
    data = get_all_clients()
    for client in data:
        response = ping_devices(client["Ip_address"], client["Running_port"])
        if response:
            data_object = create_object_for_database(client["Ip_address"], client["Running_port"],
                                                     client["Mac_address"], client["Width"], client["Height"], "Active")
        else:
            data_object = create_object_for_database(client["Ip_address"], client["Running_port"],
                                                     client["Mac_address"], client["Width"], client["Height"],
                                                     "Not Active")
        Database.new_update_connection("Clients_Collection", data_object)

def ping_devices(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        int_port = int(port)
        sock.close()
        if sock.connect_ex((host, int_port)) == 0:
            return True
        else:
            return False




if __name__ == '__main__':
    listen_for_computer_info = threading.Thread(target=listen_to_computer_info)
    listen_for_computer_info.start()
    Database.initialize()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    find_active_devices_thread = threading.Thread(target=find_active_devices)
    find_active_devices_thread.start()
    update_on_new_connection()
    app.exec_()




