import socket, traceback, threading, time, re, sys, atexit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QHBoxLayout, QWidget, QSplitter, QPushButton, QLabel, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class App:
    def __init__(self):
        self.END_CONN_CMD = "!** END_CONNECTION **!"

        self.app = QApplication([])
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        self.end_host_btn.clicked.connect(self.end_host)
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
        self.disconnect_btn.clicked.connect(self.disconn_from_friend)
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


    '''Widget callbacks'''

    def start_host(self):
        str_data = self.my_port_input.text()
        data = 0

        # Check if port number entered is valid
        try:
            data = int(str_data)
        except Exception:
            self.msg_display_area.append("ERROR: Your port number entered is not an integer.  Port number must be an integer between 1024 to 49151.")
            return
        
        if data >= 1024 and data <= 49151:
            self.msg_display_area.append("Hooray")
        else:
            self.msg_display_area.append("Invalid input for your port number.  Must be between 1024 to 49151")
            return
        
        # Bind socket and start listening
        self.my_port = data
        sock.bind((self.my_ip, self.my_port))
        listen_thread = threading.Thread(target=self.listen_thread, args=())
        listen_thread.start()

        # Update display
        self.disable_hosting_components()
        self.end_host_btn.setEnabled(True)
        self.disable_friend_sel_components()
        self.msg_input_box.setEnabled(True)
        self.enable_emoji_btns()

    
    def end_host(self):
        global sock

        # End connection
        try:
            sock.sendall(self.END_CONN_CMD.encode())
        except Exception:
            pass

        # self.end_conn()
        sock.close()

        # Update display
        self.disconn_update_display()

    
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
        if ip_regex_str.match(ip):
            self.msg_display_area.append("Good IP address")
        else:
            self.msg_display_area.append("Invalid IP address.  Formatting must be of type XXX.XXX.XXX.XXX and be within 0.0.0.0 to 255.255.255.255")
            return

        # Check if port number entered is valid
        try:
            port = int(port_input)
        except Exception:
            self.msg_display_area.append("ERROR: Friend port number entered is not an integer.  Port number must be an integer.")
            return
        
        if port >= 1024 and port <= 49151:
            self.msg_display_area.append("Hooray")
        else:
            self.msg_display_area.append("Invalid input for friend port number.  Must be between 1024 to 49151")
            return
        
        # Connect to peer
        self.friend_ip = ip
        self.friend_port = port

        try:
            sock.connect((self.friend_ip, self.friend_port))
            self.msg_display_area.append("Connection successful")
            read_thread = threading.Thread(target=self.create_read_thread, args=())
            read_thread.start()

        except Exception as e:
            print("conn_to_friend error: " + str(e))
            # self.end_conn()
            sock.close()
            self.disconn_update_display()
            self.msg_display_area.append("Connection unsuccessful:" + str(e))
            return

        
        # Update display
        self.disable_friend_sel_components()
        self.disconnect_btn.setEnabled(True)
        self.disable_hosting_components()
        self.msg_input_box.setEnabled(True)
        self.enable_emoji_btns()
    

    def disconn_from_friend(self):
        global sock

        # End connection
        sock.sendall(self.END_CONN_CMD.encode())
        # self.end_conn()
        sock.close()

        # Update display
        self.disconn_update_display()
    

    def disconn_update_display(self):
        self.enable_friend_sel_components()
        self.disconnect_btn.setDisabled(True)
        self.enable_hosting_components()
        self.end_host_btn.setDisabled(True)
        self.msg_input_box.setDisabled(True)
        self.disable_emoji_btns()
        self.clear_all_inputs()
    

    def end_conn(self):
        global sock

        try:

            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.friend_ip = ""
            self.friend_port = 0
            self.my_port = 0
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
    
    
    def enter_msg(self):
        msg = self.msg_input_box.text()

        if not msg.isspace() and msg != '':
            self.msg_display_area.append("Me: " + msg)
        
        sock.sendall(msg.encode())
        
        self.msg_input_box.clear()


    def emoji_btn_clicked(self, emoji_str):
        msg = msg = self.msg_input_box.text()
        self.msg_input_box.setText(msg + emoji_str)


    def create_read_thread(self):
        # sock = conn_or_sock # i added
        self.msg_display_area.append("Read thread started...")
        try:
            while True:
                recvd_msg = sock.recv(5000)
                msg = recvd_msg.decode()

                if (msg == self.END_CONN_CMD):
                    # self.end_conn()
                    sock.close()
                    self.disconn_update_display()
                    return

                self.msg_display_area.append("Friend:\n" + msg)
        except Exception as e:
            print("reate_read_thread error: " + str(e))
            # self.end_conn()
            # self.disconn_update_display()
            # self.msg_display_area.append("Unexpected error encounter in connection.  Connection closing...")
            return
            # pass
        


    # def connect_peer(self, sock, peer_address):
    #     try:
    #         sock.connect(peer_address)
    #         print ("Connection successful")
    #         read_thread = threading.Thread(target=create_read_thread, args=(sock, ))
    #         read_thread.start()

    #     except Exception:
    #         print ("Connection unsuccessful")

    # def connect_peer(self):
    #     try:
    #         sock.connect((self.friend_ip, self.friend_port))
    #         self.msg_display_area.append("Connection successful")
    #         read_thread = threading.Thread(target=create_read_thread, args=())
    #         read_thread.start()

    #     except Exception as e:
    #         # self.end_conn()
    #         # self.disconn_update_display()
    #         # self.msg_display_area.append("Connection unsuccessful")
    #         # print("connect_peer error: " + str(e))
    #         pass
            

    
    def listen_thread(self):
        global sock

        try:
            sock.listen(1)
            connection, peer_address = sock.accept()
            print(peer_address)
            sock.close() # I added
            sock = connection # I added
            self.msg_display_area.append("Connected to: " + peer_address[0] + ":" + str(peer_address[1]))
            read_thread = threading.Thread(target=self.create_read_thread, args=())
            read_thread.start()

        except Exception as e:
            print("listen_thread error: " + str(e))
            # self.end_conn()
            sock.close()
            self.disconn_update_display()
            self.msg_display_area.append("Unexpected error while listening for connections.  Hosting stopped...")
            
            # pass
    
# Makes sure threads and sockets close after the window closes
def on_exit_cleanup():
    sock.close()
        

if __name__ == "__main__":
    app = App()
    atexit.register(on_exit_cleanup)
    app.app.exec_()

    # Makes sure threads and sockets close after the window closes
    sock.close()
    
    # window = Window()
    # window.show()
    # sys.exit(app.exec_())














# #boolean to indicate if this peer is acting as the server or not
# connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# is_server = False

# #get the name and port the user wants to use
# name = input("Input user name: ")
# self_port = int(input("Enter the port number you want to use: "))

# self_address = ("127.0.0.1", self_port)

# #create a tcp socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(self_address)

# response = input("Do you want to host? (Y/N)")

# if response == "Y":
#     listen_thread = threading.Thread(target=listen_thread, args=(sock, ))
#     listen_thread.start()
#     listen_thread.join()
#     is_server = True
# elif response == "N":
#     #ask the user which port they want to connect to to chat with
#     peer_port = int(input("Which Port Do You Want To Chat With? "))
#     peer_address = ("127.0.0.1", peer_port)
#     connect(sock, peer_address)
# else:
#     print ("invalid input")



# #constantly let the user send messages to the other peer. Send logic also differs from client and server, so need to use the is_server boolean here too
# while True:
#     message = input()
#     # if is_server != False:
#     #     connection.sendall(message.encode())
#     # else:
#     sock.sendall(message.encode())





'''
is_server = False

    #try to connect to that port. If connection fails it isn't set up yet, and the use should instead listen for a connection from the peer
    try:
        sock.connect(peer_address)
        print ("Connection successful")

    except:
        print ("Peer not set up, listening instead...")
        sock.listen(1)
        connection, peer_address = sock.accept()
        print ("Connected to: ", peer_address)
        is_server = True

    #now spawn a thread to constantly read incoming messages. Read logic differs between client and server, so need to use the is_server boolean
    if is_server == True:
        read_thread = threading.Thread(target=create_read_thread, args=(connection, ))
    else:  
        read_thread = threading.Thread(target=create_read_thread, args=(sock, ))

    read_thread.start()
'''


