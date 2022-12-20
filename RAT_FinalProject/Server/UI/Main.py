from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QAction
from PyQt5.uic.properties import QtGui
import UI.DesktopViewer

from UI.DesktopViewer import DesktopViewer
from UI.RemoteShellExec import RemoteShell
from process_list import ProcessList
from ftps_client import FtpsClient

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('UI/MainWindow.ui', self)
        self.computerInfoList.setColumnWidth(0, 135)
        self.computerInfoList.setColumnWidth(1, 135)
        self.computerInfoList.setColumnWidth(2, 135)
        self.computerInfoList.setColumnWidth(3, 135)
        self.computerInfoList.setColumnWidth(5, 135)
        self.show()
        # self.computerInfoList.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.computerInfoList.customContextMenuRequested.connect(self.right_click_context_menu)

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
            self.computerInfoList.setItem(row, 0, QtWidgets.QTableWidgetItem(client["Ip_address"]))
            self.computerInfoList.setItem(row, 1, QtWidgets.QTableWidgetItem(client["Running_port"]))
            self.computerInfoList.setItem(row, 2, QtWidgets.QTableWidgetItem(client["Mac_address"]))
            self.computerInfoList.setItem(row, 3, QtWidgets.QTableWidgetItem(client["Width"]))
            self.computerInfoList.setItem(row, 4, QtWidgets.QTableWidgetItem(client["Height"]))
            self.computerInfoList.setItem(row, 5, QtWidgets.QTableWidgetItem(client["Status"]))

            row += 1

    def right_click_context_menu(self, pos):
        selected_row = self.get_item_selected()
        if selected_row is not None:
            contextMenu = QMenu()
            remote_desktop = contextMenu.addAction("Remote desktop")
            run_command_line = contextMenu.addAction("Command line")
            process_list = contextMenu.addAction("Process list")
            remote_file_explorer = contextMenu.addAction("Remote file explorer")
            delete_client_information = contextMenu.addAction("Delete client's information")
            action = contextMenu.exec_(self.mapToParent(pos))

            """ Getting info needed for the remote desktop viewer (ipaddress, port, width, height) """

            ipaddress = self.computerInfoList.item(selected_row, 0).text()
            port = self.computerInfoList.item(selected_row, 1).text()
            width = self.computerInfoList.item(selected_row, 3).text()
            height = self.computerInfoList.item(selected_row, 4).text()
            if action == remote_desktop:
                dv = DesktopViewer(ipaddress, port, width, height)
            elif action == run_command_line:
                self.remote_window = RemoteShell()
                self.remote_window.show()
            elif action == process_list:
                processList = ProcessList()
                processList.write_file()
            elif action == remote_file_explorer:
                ftpsClient = FtpsClient(ipaddress, port)
            elif action == delete_client_information:
                print("")

    def get_item_selected(self):
        return self.computerInfoList.currentRow()


"""app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()"""
