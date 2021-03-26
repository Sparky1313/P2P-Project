from _thread import *
import threading
from socket import *
import tkinter as tk



class GUI:
    def __init__(self):

        self.window = tk.Tk()
        self.window.withdraw()

        self.login = tk.Toplevel()
        self.login.title("Login")
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 500, height = 500)
        self.name_label = tk.Label(self.login, text = "Name: ", font = "Helvetica 16")
        self.name_label.place(relheight = 0.3, relx = 0.4, rely = 0.2)
        self.window.mainloop()


def client_func():
    client_socket = socket(AF_INET, SOCK_STREAM)
    # I need a lock for this I think
    client_port = input("Client port: ")
    client_socket.bind(('127.0.0.1', int(client_port)))
    decision = input("Connect to a friend?: ")

    if decision == 'Y':
        friend_ip = input("Enter IP address: ")
        friend_port = input("Port number: ")
        client_socket.connect((friend_ip, int(friend_port)))
        client_socket.send("Hi".encode())
    else:
        print("Okay waiting... then")
    # client_socket.setblocking(0)
    
def srvr_func():
    srvr_socket = socket(AF_INET, SOCK_STREAM)
    # I need a lock for this I think
    srvr_port = input("Input server port: ")
    srvr_socket.bind(('127.0.0.1', int(srvr_port)))
    # srvr_socket.setblocking(0)
    srvr_socket.listen(1)

    while True:
        conn_sock, addr = srvr_socket.accept()

        start_new_thread(srvr_thread, (conn_sock,))


def srvr_thread(sckt):
    msg = sckt.recv(1024).decode()
    print("Bro: " + msg)

window = GUI()
start_new_thread(client_func, ())
start_new_thread(srvr_func, ())

while True:
    x = 1




