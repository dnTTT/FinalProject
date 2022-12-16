import traceback

from PyQt5 import QtWidgets, uic
import sys
import socket
import logging

class RemoteShell(QtWidgets.QWidget):
    def __init__(self):
        super(RemoteShell, self).__init__()
        uic.loadUi('UI/Test.ui', self)
        self.show()
        self.txtCommand.returnPressed.connect(self.update_text_field_result)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("192.168.2.75", 6666))
        self.s.sendall("command_line".encode())
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

    def update_text_field_result(self):
        command = self.txtCommand.text()
        if command != "":
            self.txtCommand.setText("")
            if command == "EXIT":
                sys.exit()
            else:
                self.txtResult.append(f"Sending command: {command}")
                encoded_data = command.encode()

                self.s.sendall(encoded_data)

                #self.data = self.s.recv(1024)

                size_len = int.from_bytes(self.s.recv(1), byteorder='big')
                size = int.from_bytes(self.s.recv(size_len), byteorder='big')
                self.data = self.recvall(self.s, size)

                #print(self.data)
            if self.data != "":
                for line in self.data.splitlines():
                    self.txtResult.append(str(line.decode('utf-8')))


"""app = QtWidgets.QApplication(sys.argv)
window = RemoteShell()
app.exec_()"""