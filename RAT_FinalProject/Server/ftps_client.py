import socket

import win32api
from easygui import *
from PyQt5.QtCore import QProcess


class FtpsClient:
    ip_address = ""
    port = 0

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = int(port)
        self.main()

    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.ip_address, self.port))
                sock.sendall("sftp_server".encode())
                data = sock.recv(1024)
                if data.decode() == "Started":
                    # message to be displayed
                    text = "Insert FTP login"

                    # window title
                    title = "FTP Login"

                    # list of entry fields
                    fields = ["Username", "Password"]

                    # creating a multi password box
                    output = multpasswordbox(text, title, fields)
                    if output:
                        p = QProcess()
                        p.startDetached("C:\\Windows\\explorer.exe",
                                        [f"ftp://{output[0]}:{output[1]}@{self.ip_address}:2221"])
                    else:
                        win32api.MessageBox(0, 'Error', 'Not all fields were filled')

            finally:
                sock.close()
