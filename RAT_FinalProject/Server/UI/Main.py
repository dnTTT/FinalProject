from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QAction
from PyQt5.uic.properties import QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('UI/MainWindow.ui', self)
        self.computerInfoList.setColumnWidth(0, 135)
        self.computerInfoList.setColumnWidth(1, 135)
        self.computerInfoList.setColumnWidth(2, 135)
        self.computerInfoList.setColumnWidth(3, 135)
        self.computerInfoList.setColumnWidth(5, 135)

        #self.computerInfoList.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.computerInfoList.customContextMenuRequested.connect(self.right_click_context_menu)


        self.show()

        """object = [{
            "Hostname": "hostname",
            "Ip_address": "ip_address",
            "Running_port": "running_port",
            "Mac_address": "mac_address"
        },
            {"Hostname": "asdadasd",
                        "Ip_address": "asdads",
        "Running_port": "asd",
        "Mac_address": "asdadad"}
        ]
        self.load_data_to_table(object)"""

    def load_data_to_table(self, data):
        row = 0
        self.computerInfoList.setRowCount(len(data))

        for client in data:
            self.computerInfoList.setItem(row, 0, QtWidgets.QTableWidgetItem(client["Hostname"]))
            self.computerInfoList.setItem(row, 1, QtWidgets.QTableWidgetItem(client["Ip_address"]))
            self.computerInfoList.setItem(row, 2, QtWidgets.QTableWidgetItem(client["Running_port"]))
            self.computerInfoList.setItem(row, 3, QtWidgets.QTableWidgetItem(client["Mac_address"]))
            row += 1

    def right_click_context_menu(self, pos):
        selected_row = self.get_item_selected()
        if selected_row != None:
            print(self.computerInfoList.item(selected_row, 0).text())
            contextMenu = QMenu()
            remote_desktop = contextMenu.addAction("Remote desktop")
            run_command_line = contextMenu.addAction("Command line")
            process_list = contextMenu.addAction("Process list")
            remote_file_explorer = contextMenu.addAction("Remote file explorer")
            action = contextMenu.exec_(self.mapToParent(pos))



    def get_item_selected(self):
        return self.computerInfoList.currentRow()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()