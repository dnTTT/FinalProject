import socket
import win32api

class ProcessList:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = int(port)
        self.result = ""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ip_address, self.port))
        self.data = ""

    def recvall(self, conn, length):
        """ Retrieve all bytes. """

        buf = b''
        while len(buf) < length:
            data = conn.recv(length - len(buf))
            if not data:
                return data
            buf += data
        return buf

    def write_file(self):
        command = "processes"
        encoded_data = command.encode()
        self.s.sendall(encoded_data)

        size_len = int.from_bytes(self.s.recv(1), byteorder='big')
        size = int.from_bytes(self.s.recv(size_len), byteorder='big')
        self.data = self.recvall(self.s, size)
        with open('processList.txt', 'w') as f:
            f.write(self.data.decode())
            win32api.MessageBox(0, 'Completed', 'Finished writing to the file')
            f.close()
