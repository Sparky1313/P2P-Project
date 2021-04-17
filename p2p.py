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


        # My selection components and layout
        # Components
        self.my_port_input = QLineEdit("Enter your port to run on...")
        self.my_port_input_lbl = QLabel("Enter your port number:")
        self.sign_in_btn = QPushButton("Sign In")

        self.my_port_input_lbl.setBuddy(self.my_port_input)
        self.sign_in_btn.clicked.connect(self.sign_in)

        my_sel_layout = QHBoxLayout()
        my_sel_layout.addWidget(self.my_port_input_lbl)
        my_sel_layout.addWidget(self.my_port_input)
        my_sel_layout.addWidget(self.sign_in_btn)


        # Friend selection components and layout
        # Components
        self.friend_ip_input = QLineEdit("Enter friend's IP address to connect to...")
        self.friend_port_input = QLineEdit("Enter friend's port number to connect to...")
        self.friend_ip_input_lbl = QLabel("Enter friend's IP Address:")
        self.friend_port_input_lbl = QLabel("Enter friend's port number:")
        self.connect_btn = QPushButton("Connect")
        self.end_btn = QPushButton("End Connection")

        self.friend_ip_input_lbl.setBuddy(self.friend_ip_input)
        self.friend_port_input_lbl.setBuddy(self.friend_port_input)
        self.connect_btn.clicked.connect(self.conn_to_friend)
        

        # Layout
        friend_sel_layout = QHBoxLayout()
        friend_sel_layout.addWidget(self.friend_ip_input_lbl)
        friend_sel_layout.addWidget(self.friend_ip_input)
        friend_sel_layout.addWidget(self.friend_port_input_lbl)
        friend_sel_layout.addWidget(self.friend_port_input)
        friend_sel_layout.addWidget(self.connect_btn)
        friend_sel_layout.addWidget(self.end_btn)
        

        # Start and end connection components and layout
        # Components
        # self.connect_btn = QPushButton("Connect")
        # self.end_btn = QPushButton("End Connection")

        # Layout
        # connection_layout = QHBoxLayout()
        # connection_layout.addWidget(self.connect_btn)
        # connection_layout.addWidget(self.end_btn)


        # Message area components and layout
        # Components
        self.msg_display_area = QTextEdit("Message Display")
        self.msg_input_box = QLineEdit("Message Input")
        self.msg_input_box_lbl = QLabel("Input message here:")

        self.msg_display_area.setReadOnly(True)
        self.msg_input_box.returnPressed.connect(self.enter_msg)
        self.msg_input_box_lbl.setBuddy(self.msg_input_box)

        #Layout
        msg_input_layout = QHBoxLayout()
        msg_input_layout.addWidget(self.msg_input_box_lbl)
        msg_input_layout.addWidget(self.msg_input_box)

        msg_area_layout = QVBoxLayout()
        msg_area_layout.addWidget(self.msg_display_area)
        msg_area_layout.addLayout(msg_input_layout)


        # Emoji components and layout
        # Components
        self.smile_btn = QPushButton("Smile")
        self.laugh_btn = QPushButton("Laugh")
        self.cry_btn = QPushButton("Cry")
        self.angry_btn = QPushButton("Angry")

        # Layout
        emoji_layout = QHBoxLayout()
        emoji_layout.addWidget(self.smile_btn)
        emoji_layout.addWidget(self.laugh_btn)
        emoji_layout.addWidget(self.cry_btn)
        emoji_layout.addWidget(self.angry_btn)



        # Window layout
        window_layout = QVBoxLayout()
        window_layout.addLayout(my_sel_layout)
        window_layout.addLayout(friend_sel_layout)
        # window_layout.addLayout(connection_layout)
        window_layout.addLayout(msg_area_layout)
        window_layout.addLayout(emoji_layout)

        
        # Create and show window
        self.window = QWidget()
        self.window.setLayout(window_layout)
        self.window.setWindowTitle("P2P Chat App")
        self.window.show()

    #Widget callbacks
    def sign_in(self):
        str_data = self.my_port_input.text()
        data = 0

        try:
            data = int(str_data)
        except:
            self.msg_display_area.append("ERROR: Your port number entered is not an integer.  Port number must be an integer between 1024 to 49151.")
            return
        

        if data >= 1024 and data <= 49151:
            self.msg_display_area.append("Hooray")
            
        else:
            self.msg_display_area.append("Invalid input for your port number.  Must be between 1024 to 49151")
        #start running server
    
    def conn_to_friend(self):
        ip_input = self.friend_ip_input.text()
        port_input = self.friend_port_input.text()

        # Regex used to check for valid IP address
        ip_regex_str = re.compile("^(([0-2][0-5][0-5]|[0-1]\d{2}|\d{1,2})\.){3}([0-2][0-5][0-5]|[01]\d{2}|\d{1,2})$")

        if ip_regex_str.match(ip_input):
            self.msg_display_area.append("Good IP address")
        else:
            self.msg_display_area.append("Invalid IP address.  Formatting must be of type XXX.XXX.XXX.XXX and be within 0.0.0.0 to 255.255.255.255")
            return

        try:
            data = int(port_input)
        except:
            self.msg_display_area.append("ERROR: Friend port number entered is not an integer.  Port number must be an integer.")
            return
        

        if data >= 1024 and data <= 49151:
            self.msg_display_area.append("Hooray")
            
        else:
            self.msg_display_area.append("Invalid input for friend port number.  Must be between 1024 to 49151")
    
    
    def enter_msg(self):
        msg = self.msg_input_box.text()
        

        if not msg.isspace() and msg != '':
            self.msg_display_area.append("Me: " + msg)



if __name__ == "__main__":

    app = App()
    app.app.exec_()
    # window = Window()
    # window.show()
    # sys.exit(app.exec_())