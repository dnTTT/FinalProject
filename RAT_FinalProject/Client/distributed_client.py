import socket
from getmac import get_mac_address as gma
import random

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

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


def start_listening_for_commands():
    running_port = return_not_used_port()
    send_computer_information(running_port)


def send_computer_information(running_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        hostname = socket.getfqdn()
        # Wait to see if workes with outside lan connection
        ip_address = socket.gethostbyname(hostname)
        mac_address = gma()
        data_to_send = [hostname, ip_address, str(running_port), mac_address]
        encoded_data = '||'.join(data_to_send).encode()
        s.sendall(encoded_data)
        data = s.recv(1024)  # Close connection

def main():
    start_listening_for_commands()

if __name__ == '__main__':
    main()
