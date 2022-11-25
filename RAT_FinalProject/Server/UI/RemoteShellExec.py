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
        self.s.connect(("192.168.1.25", 6666))
        self.data = ""

    def update_text_field_result(self):
        command = self.txtCommand.text()
        if command != "":
            self.txtCommand.setText("")
            if command == "EXIT":
                sys.exit()
            else:
                self.txtResult.setPlainText(f"Sending command: {command}")
                encoded_data = command.encode()
                self.s.sendall(encoded_data)

                self.data = self.s.recv(1024)

                #print(self.data)
            if self.data != "":
                for line in self.data.splitlines():
                    self.txtResult.append(str(line.decode('utf-8')))


"""app = QtWidgets.QApplication(sys.argv)
window = RemoteShell()
app.exec_()"""