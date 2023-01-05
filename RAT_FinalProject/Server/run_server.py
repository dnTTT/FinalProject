import os
import socket

import win32api

from Handler.database import Database
from PyQt5 import QtWidgets, uic
import sys
from UI.Main import MainWindow
import threading
from contextlib import closing
import ssl
from Handler.encryption import EncryptionHandler

HOST = "192.168.1.173"
PORT = 65432

def listen_to_computer_info():
    # SSLContext.wrap not working because hostname mismatch (on dynamic local ip), update later with a web server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))

        try:
            sock.listen(5)
            print('Server started.')

            while 'connected':
                client_sock, client_address = sock.accept()
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(certfile="mycert.pem")
                context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
                context.set_ciphers('AES256+ECDH:AES256+EDH')
                ssl_client_sock = context.wrap_socket(client_sock, server_side=True)
                """ssl_client_sock = ssl.wrap_socket(client_sock,
                                                  server_side=True,
                                                  certfile="../certificates2/server.crt",
                                                  keyfile="../certificates2/server.key")"""

                data = ssl_client_sock.recv(1024)
                if len(data) > 0:
                    # Decode information received, and split by ||
                    ip_address, running_port, mac_address, width, height = data.decode("Utf-8").split("||")
                    data_object = create_object_for_database(ip_address, running_port, mac_address, width,
                                                             height, "Active", None, "Encrypt")
                    insert_on_database("Clients_Collection", data_object)
                    #find_active_devices_thread = threading.Thread(target=find_active_devices)
                    #sfind_active_devices_thread.start()
                    find_active_devices()
                    update_on_new_connection()
                win32api.MessageBox(0, f'New client connected: {client_address[0]}', 'New client')


        finally:
            client_sock.close()

def get_all_clients():
    return Database.get_all("Clients_Collection")


def update_on_new_connection():
    populate_list_data = get_all_clients()
    data_list = []
    for x in populate_list_data:
        x["Ip_address"] = encryption_handler.decrypt(x["Ip_address"])
        x["Mac_address"] = encryption_handler.decrypt(x["Mac_address"])
        data_list.append(x)
    window.load_data_to_table(data_list)


def insert_on_database(collection, data):
    Database.new_update_connection(collection, data)


def create_object_for_database(ip_address, running_port, mac_address, width, height, status, uid, method=None):
    if method == "Encrypt":
        encrypted_ipaddress = encryption_handler.encrypt(ip_address)
        encrypted_mac_address = encryption_handler.encrypt(mac_address)
    elif method == "Decrypt":
        encrypted_ipaddress = encryption_handler.decrypt(ip_address)
        encrypted_mac_address = encryption_handler.decrypt(mac_address)
    else:
        encrypted_ipaddress = ip_address
        encrypted_mac_address = mac_address

    object = {
        "Ip_address": encrypted_ipaddress,
        "Running_port": running_port,
        "Mac_address": encrypted_mac_address,
        "Width": width,
        "Height": height,
        "Status": status,
        "_id": uid
    }
    return object

def find_active_devices():
    data = get_all_clients()
    for client in data:
        ip_address = encryption_handler.decrypt(client["Ip_address"])
        response = ping_devices(ip_address, client["Running_port"])
        if response:
            data_object = create_object_for_database(client["Ip_address"], client["Running_port"],
                                                     client["Mac_address"], client["Width"], client["Height"], "Active"
                                                     , client["_id"])

            Database.new_update_connection("Clients_Collection", data_object)
        else:
            """data_object = create_object_for_database(client["Ip_address"], client["Running_port"],
                                                     client["Mac_address"], client["Width"], client["Height"],
                                                     "Not Active", client["_id"])"""
            Database.delete("Clients_Collection", client["_id"])


def ping_devices(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        int_port = int(port)
        #sock.close()
        if sock.connect_ex((host, int_port)) == 0:
            return True
        else:
            return False




if __name__ == '__main__':
    encryption_handler = EncryptionHandler()
    password = encryption_handler.password_box()
    if password:
        listen_for_computer_info = threading.Thread(target=listen_to_computer_info)
        listen_for_computer_info.start()
        Database.initialize()
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        find_active_devices_thread = threading.Thread(target=find_active_devices)
        find_active_devices_thread.start()
        #find_active_devices()
        update_on_new_connection()
        app.exec_()
    else:
        os._exit(1)




