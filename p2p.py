import socket, traceback, threading, time, re, sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QHBoxLayout, QWidget, QSplitter, QPushButton, QLabel, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit

# self.app = QApp

class ListenThread(QThread):
    sig = pyqtSignal(object)

    def __init__(self, socket):
        QThread.__init__(self)
        self.socket = socket
    
    def run(self):
        with self.socket:
            while(True):
                try:
                    data = self.socket.recv(5000).decode()
                except:
                    self.socket.close()
                    return
                
                if data == "$--END SESSION--$":
                    self.socket.sendall("$--END SESSION--$")
                    self.socket.close()
                
                self.sig.emit(data)


class App:
    def __init__(self):
        self.app = QApplication([])

        # Message area layout
        message_area_layout = QVBoxLayout()
        message_area_layout.addWidget(QTextEdit())
        message_area_layout.addWidget(QLineEdit())


        # Host selection components and layout
        self.ip_field = QLineEdit("Enter IP address to connect to...")
        self.ip_field = QLineEdit("Enter port number to connect to...")
        self.connect_btn = QPushButton("Connect")

        host_selection_layout = QHBoxLayout()
        host_selection_layout.addWidget(QPushButton("User 1"))
        host_selection_layout.addWidget(QPushButton("User 2"))

        # Window layout
        window_layout = QVBoxLayout()
        window_layout.addLayout(message_area_layout)
        window_layout.addLayout(host_selection_layout)

        # Create and show window
        self.window = QWidget()
        self.window.setLayout(window_layout)
        self.window.show()






if __name__ == "__main__":

    app = App()
    app.app.exec_()
    # window = Window()
    # window.show()
    # sys.exit(app.exec_())