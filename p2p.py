from _thread import *
import threading
from socket import *
import tkinter as tk
import select

# Use these values just for testing.
# In reality you would have different IP addresses, but
# could use the same ports.
derek_ip = "127.0.0.1"
derek_srvr_port = 12000
derek_client_port = 12001

trevor_ip = "127.0.0.1"
trevor_srvr_port = 12002
trevor_client_port = 12003



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


def client_func(user):
    client_socket = socket(AF_INET, SOCK_STREAM)

    if user == "Derek":
        client_socket.bind((derek_ip, derek_client_port))

        try:
            client_socket.connect((trevor_ip, trevor_srvr_port))
        except:
            client_socket.close()
            srvr_func(derek_ip, derek_srvr_port)
    elif user == "Trevor":
        client_socket.bind((trevor_ip, trevor_client_port))

        try:
            client_socket.connect((derek_ip, derek_srvr_port))
        except:
            client_socket.close()
            srvr_func(trevor_ip, trevor_srvr_port)
    
    client_socket.setblocking(0)
    client_socket.send("Hi".encode())

    while True:
        # client_socket.send("Hi".encode())
        # print(client_socket.recv(1024).decode())
        polling(client_socket)

# def client_func():
#     client_socket = socket(AF_INET, SOCK_STREAM)
#     # I need a lock for this I think
#     client_port = input("Client port: ")
#     client_socket.bind(('127.0.0.1', int(client_port)))
#     decision = input("Connect to a friend?: ")

#     if decision == 'Y':
#         friend_ip = input("Enter IP address: ")
#         friend_port = input("Port number: ")
#         # client_socket.connect((friend_ip, int(friend_port)))
#         # client_socket.send("Hi".encode())
#     else:
#         print("Okay waiting... then")
#     # client_socket.setblocking(0)


def srvr_func(ip, port):
    srvr_socket = socket(AF_INET, SOCK_STREAM)
    srvr_socket.bind((ip, port))
    # srvr_socket.setblocking(0)
    srvr_socket.listen(1)

    while True:
        conn_sock, addr = srvr_socket.accept()
        conn_sock.setblocking(0)

        start_new_thread(polling, (conn_sock,))
# def srvr_func():
#     srvr_socket = socket(AF_INET, SOCK_STREAM)
#     # I need a lock for this I think
#     srvr_port = input("Input server port: ")
#     srvr_socket.bind(('127.0.0.1', int(srvr_port)))
#     # srvr_socket.setblocking(0)
#     srvr_socket.listen(1)

#     while True:
#         conn_sock, addr = srvr_socket.accept()

#         start_new_thread(srvr_thread, (conn_sock,))


def srvr_thread(sckt):
    while True:
        msg = ""
        msg = sckt.recv(1024).decode()
        print(msg)
        sckt.send("Yo".encode())
        # I need a lock for this I think

def polling(sckt):
    while True:
        readable, writable, exceptional = select.select([sckt], [sckt], [sckt])

        for item in writable:
            


name = input("Input user name: ")
client_func(name)
# window = GUI()
# start_new_thread(client_func, ())
# start_new_thread(srvr_func, ())

# while True:
#     x = 1





