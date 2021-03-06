import socket, traceback, threading, time, re, sys, atexit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QHBoxLayout, QWidget, QSplitter, QPushButton, QLabel, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# A QThread that reads incoming messages and lets the main thread
# know that the messages need to be append to the message display area.
class ReadThread(QThread):
    new_msg = pyqtSignal(str)
    req_end = pyqtSignal()

    def __init__(self, end_cmd, end_cmd_ack):
        QThread.__init__(self)
        self.end_cmd = end_cmd
        self.end_cmd_ack =end_cmd_ack
    

    def run(self):
        try:
            while True:
                recvd_msg = sock.recv(5000)
                msg = recvd_msg.decode()

                if msg == self.end_cmd:
                    self.new_msg.emit(self.end_cmd_ack)
                    self.req_end.emit()
                    return
                
                if msg == self.end_cmd_ack:
                    self.req_end.emit()
                    return
                
                self.new_msg.emit("Friend:\n" + msg)
        except Exception as e:
            # print("reate_read_thread error: " + str(e))
            self.req_end.emit()
            return



# A QThread that listens for sockets trying to make a connection
# when the user is the host.
class ListenThread(QThread):
    new_thread = pyqtSignal()
    req_end = pyqtSignal()
    conn_made = pyqtSignal(str)
    sent_err_msg = pyqtSignal(str) # This component is not hooked up


    def __init__(self):
        QThread.__init__(self)
    

    def run(self):
        global sock

        try:
            sock.listen(1)
            connection, peer_address = sock.accept()
            sock.close()
            sock = connection
            self.conn_made.emit(peer_address[0] + ":" + str(peer_address[1]) + " CONNECTED")
            self.new_thread.emit()
        except Exception as e:
            # print("listen_thread error: " + str(e))
            self.req_end.emit()
            self.sent_err_msg.emit("Unexpected error while listening for connections.  Hosting stopped...")

    
# The main application gui and logic
class App:
    def __init__(self):
        self.END_CONN_CMD = "!** END_CONNECTION **!"
        self.END_CONN_CMD_ACK = "!** END_ACK **!"

        self.q_app = QApplication([])
        self.my_ip = "127.0.0.1"
        self.my_port = 0
        self.friend_ip = ""
        self.friend_port = 0


        '''Start components and layout'''

        ###### Hosting components and layout ######

        # ---Components setup---
        self.my_port_input = QLineEdit("Enter your port to run on...")
        self.my_port_input_lbl = QLabel("Enter your port number:")
        self.start_host_btn = QPushButton("Host")
        self.end_host_btn = QPushButton("End Hosting")

        # ---Initial function calls---
        self.my_port_input_lbl.setBuddy(self.my_port_input)
        self.start_host_btn.clicked.connect(self.start_host)
        self.end_host_btn.clicked.connect(self.send_end)
        self.end_host_btn.setDisabled(True)

        # ---Layout setup---
        my_sel_layout = QHBoxLayout()
        my_sel_layout.addWidget(self.my_port_input_lbl)
        my_sel_layout.addWidget(self.my_port_input)
        my_sel_layout.addWidget(self.start_host_btn)
        my_sel_layout.addWidget(self.end_host_btn)

        ################################################


        ###### Friend selection components and layout ######

        # ---Components setup---
        self.friend_ip_input = QLineEdit("Enter friend's IP address to connect to...")
        self.friend_port_input = QLineEdit("Enter friend's port number to connect to...")
        self.friend_ip_input_lbl = QLabel("Enter friend's IP Address:")
        self.friend_port_input_lbl = QLabel("Enter friend's port number:")
        self.connect_btn = QPushButton("Connect")
        self.disconnect_btn = QPushButton("End Connection")

        # ---Initial function calls---
        self.friend_ip_input_lbl.setBuddy(self.friend_ip_input)
        self.friend_port_input_lbl.setBuddy(self.friend_port_input)
        self.connect_btn.clicked.connect(self.conn_to_friend)
        self.disconnect_btn.clicked.connect(self.send_end)
        self.enable_friend_sel_components()
        self.disconnect_btn.setDisabled(True)

        # ---Layout setup---
        friend_sel_layout = QHBoxLayout()
        friend_sel_layout.addWidget(self.friend_ip_input_lbl)
        friend_sel_layout.addWidget(self.friend_ip_input)
        friend_sel_layout.addWidget(self.friend_port_input_lbl)
        friend_sel_layout.addWidget(self.friend_port_input)
        friend_sel_layout.addWidget(self.connect_btn)
        friend_sel_layout.addWidget(self.disconnect_btn)

        ################################################


        ###### Message area components and layout ######

        # ---Components setup---
        self.msg_display_area = QTextEdit("Message Display")
        self.msg_input_box = QLineEdit("Message Input")
        self.msg_input_box_lbl = QLabel("Input message here:")

        # ---Initial function calls
        self.msg_display_area.setReadOnly(True)
        self.msg_input_box.returnPressed.connect(self.enter_msg)
        self.msg_input_box_lbl.setBuddy(self.msg_input_box)
        self.msg_input_box.setDisabled(True)

        # ---Layout setup---
        msg_input_layout = QHBoxLayout()
        msg_input_layout.addWidget(self.msg_input_box_lbl)
        msg_input_layout.addWidget(self.msg_input_box)
        msg_area_layout = QVBoxLayout()
        msg_area_layout.addWidget(self.msg_display_area)
        msg_area_layout.addLayout(msg_input_layout)

        ################################################


        ###### Emoji components and layout ######

        # ---Components setup---
        self.thumbs_up_btn = QPushButton("\U0001F44D")
        self.thumbs_down_btn = QPushButton("\U0001F44E")
        self.smile_btn = QPushButton("\U0001F600")
        self.laugh_btn = QPushButton("\U0001F923")
        self.cry_btn = QPushButton("\U0001F62D")
        self.angry_btn = QPushButton("\U0001F620")

        # ---Initial function calls
        self.thumbs_up_btn.clicked.connect(lambda: self.emoji_btn_clicked("\U0001F44D"))
        self.thumbs_down_btn.clicked.connect(lambda: self.emoji_btn_clicked("\U0001F44E"))
        self.smile_btn.clicked.connect(lambda: self.emoji_btn_clicked("\U0001F600"))
        self.laugh_btn.clicked.connect(lambda: self.emoji_btn_clicked("\U0001F923"))
        self.cry_btn.clicked.connect(lambda: self.emoji_btn_clicked("\U0001F62D"))
        self.angry_btn.clicked.connect(lambda: self.emoji_btn_clicked("\U0001F620"))
        self.disable_emoji_btns()
        
        # ---Layout setup---
        emoji_layout = QHBoxLayout()
        emoji_layout.addWidget(self.thumbs_up_btn)
        emoji_layout.addWidget(self.thumbs_down_btn)
        emoji_layout.addWidget(self.smile_btn)
        emoji_layout.addWidget(self.laugh_btn)
        emoji_layout.addWidget(self.cry_btn)
        emoji_layout.addWidget(self.angry_btn)

        ################################################


        ###### Window components and layout ######

        # ---Layout setup---
        window_layout = QVBoxLayout()
        window_layout.addLayout(my_sel_layout)
        window_layout.addLayout(friend_sel_layout)
        window_layout.addLayout(msg_area_layout)
        window_layout.addLayout(emoji_layout)
        
        # ---Components setup---
        self.window = QWidget()
        self.window.setLayout(window_layout)
        self.window.setWindowTitle("P2P Chat App")
        self.window.show()

        ################################################

        ''' End components and layout '''


    '''Widget callbacks and application functions'''

    # Ensures a valid entry is made for hosting and
    # makes the user listen for connections on the specified port number
    def start_host(self):
        str_data = self.my_port_input.text()
        data = 0

        # Check if port number entered is valid
        try:
            data = int(str_data)
        except Exception:
            self.append_msg("ERROR: Your port number entered is not an integer.  Port number must be an integer between 1024 to 49151.")
            return
        
        if data < 1024 or data > 49151:
            self.append_msg("ERROR: Invalid input for your port number.  Must be between 1024 to 49151.")
            return
        
        # Bind socket and start listening
        self.my_port = data
        sock.bind((self.my_ip, self.my_port))
        self.listen_thread = ListenThread()
        self.listen_thread.new_thread.connect(self.create_read_thread)
        self.listen_thread.conn_made.connect(self.append_msg)
        self.listen_thread.start()

        # Update display
        self.disable_hosting_components()
        self.end_host_btn.setEnabled(True)
        self.disable_friend_sel_components()
        self.msg_input_box.setEnabled(True)
        self.enable_emoji_btns()

    # Sends out a message that let's the connected friend
    # know that the user is ending the connection and then
    # starts the process of ending the connection.
    def send_end(self):
        global sock

        # End connection
        try:
            sock.sendall(self.END_CONN_CMD.encode())
        except Exception:
            pass

        self.end_conn()

    
    # Helper method for changing display
    def enable_hosting_components(self):
        self.my_port_input.setEnabled(True)
        self.start_host_btn.setEnabled(True)
        self.end_host_btn.setEnabled(True)


    # Helper method for changing display
    def disable_hosting_components(self):
        self.my_port_input.setDisabled(True)
        self.start_host_btn.setDisabled(True)
        self.end_host_btn.setDisabled(True)


    def conn_to_friend(self):
        ip = self.friend_ip_input.text()
        port_input = self.friend_port_input.text()
        port = 0

        # Regex used to compare against for valid IP address
        ip_regex_str = re.compile("^(([0-2][0-5][0-5]|[0-1]\d{2}|\d{1,2})\.){3}([0-2][0-5][0-5]|[01]\d{2}|\d{1,2})$")

        # Check if IP address entered is valid
        if not ip_regex_str.match(ip):
            self.append_msg("ERROR: Invalid IP address.  Formatting must be of type XXX.XXX.XXX.XXX and be within 0.0.0.0 to 255.255.255.255")
            return

        # Check if port number entered is valid
        try:
            port = int(port_input)
        except Exception:
            self.append_msg("ERROR: Friend port number entered is not an integer.  Port number must be an integer.")
            return
        
        if port < 1024 or port > 49151:
            self.append_msg("ERROR: Invalid input for your port number.  Must be between 1024 to 49151.")
            return
        
        # Connect to peer
        self.friend_ip = ip
        self.friend_port = port

        try:
            sock.connect((self.friend_ip, self.friend_port))
            self.append_msg("CONNECTION SUCCESSFUL")
            self.create_read_thread()
        except Exception as e:
            # print("conn_to_friend error: " + str(e))
            self.end_conn()
            self.append_msg("CONNECTION UNSUCCESSFUL:" + str(e))
            return

        
        # Update display
        self.disable_friend_sel_components()
        self.disconnect_btn.setEnabled(True)
        self.disable_hosting_components()
        self.msg_input_box.setEnabled(True)
        self.enable_emoji_btns()
 
    
    # Updates the display appropriately when the connection
    # between user and friend is ended.
    def disconn_update_display(self):
        self.enable_friend_sel_components()
        self.disconnect_btn.setDisabled(True)
        self.enable_hosting_components()
        self.end_host_btn.setDisabled(True)
        self.msg_input_box.setDisabled(True)
        self.disable_emoji_btns()
        self.clear_all_inputs()
    

    # Appends the msg parameter to the message display area.
    def append_msg(self, msg):
        self.msg_display_area.append(msg + "\n")


    # Closes the socket being used for connections, 
    # resets corresponding variables involved in the connection,
    # and updates the display to reflect the disconnection.
    def end_conn(self):
        global sock

        try:
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.friend_ip = ""
            self.friend_port = 0
            self.my_port = 0
            self.disconn_update_display()
        except Exception as e:
            print("end_conn error: " + str(e))

    
    # Helper method for changing display
    def enable_friend_sel_components(self):
        self.friend_ip_input.setEnabled(True)
        self.friend_port_input.setEnabled(True)
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(True)


    # Helper method for changing display
    def disable_friend_sel_components(self):
        self.friend_ip_input.setDisabled(True)
        self.friend_port_input.setDisabled(True)
        self.connect_btn.setDisabled(True)
        self.disconnect_btn.setDisabled(True)
    

    # Helper method for changing display
    def enable_emoji_btns(self):
            self.thumbs_up_btn.setEnabled(True)
            self.thumbs_down_btn.setEnabled(True)
            self.smile_btn.setEnabled(True)
            self.laugh_btn.setEnabled(True)
            self.cry_btn.setEnabled(True)
            self.angry_btn.setEnabled(True)


    # Helper method for changing display
    def disable_emoji_btns(self):
        self.thumbs_up_btn.setDisabled(True)
        self.thumbs_down_btn.setDisabled(True)
        self.smile_btn.setDisabled(True)
        self.laugh_btn.setDisabled(True)
        self.cry_btn.setDisabled(True)
        self.angry_btn.setDisabled(True)


    # Clears all input fields
    def clear_all_inputs(self):
        self.my_port_input.clear()
        self.friend_ip_input.clear()
        self.friend_port_input.clear()
        self.msg_display_area.clear()
        self.msg_input_box.clear()
    

    # Handles validation of entry, sends message to friend, and
    # ensures the message is displayed on screen.
    def enter_msg(self):
        msg = self.msg_input_box.text()

        if not msg.isspace() and msg != '':
            self.append_msg("Me:\n" + msg)
        
        sock.sendall(msg.encode())
        self.msg_input_box.clear()


    # Adds the emoji to the user's message
    def emoji_btn_clicked(self, emoji_str):
        msg = msg = self.msg_input_box.text()
        self.msg_input_box.setText(msg + emoji_str)


    # Creates and starts a thread where the socket reads incoming messages.
    def create_read_thread(self):
        self.read_thread = ReadThread(self.END_CONN_CMD, self.END_CONN_CMD_ACK)
        self.read_thread.new_msg.connect(self.append_msg)
        self.read_thread.req_end.connect(self.end_conn)
        self.read_thread.start()


    
# Makes sure threads and sockets close after the window closes
def on_exit_cleanup():
    sock.close()
        

if __name__ == "__main__":
    app = App()
    atexit.register(on_exit_cleanup)
    app.q_app.exec_()

    # Makes sure threads and sockets close after the window closes
    sock.close()