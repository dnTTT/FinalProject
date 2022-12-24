import socket
import threading
import os

process_list = ""


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
                    thread = threading.Thread(target=return_process_list)
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


if __name__ == '__main__':
    process_list_service("localhost", 10300)
