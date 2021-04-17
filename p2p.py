import socket
import threading


def create_read_thread(conn_or_sock):
    print("Read thread started...")
    while True:
        recieved_message = conn_or_sock.recv(1024)
        print (recieved_message.decode())


def connect(sock, peer_address):
    try:
        sock.connect(peer_address)
        print ("Connection successful")
        read_thread = threading.Thread(target=create_read_thread, args=(sock, ))
        read_thread.start()

    except:
        print ("Connection unsuccessful")


def listen_thread(sock):
    global connection
    
    sock.listen(1)
    connection, peer_address = sock.accept()
    print ("Connected to: ", peer_address)
    read_thread = threading.Thread(target=create_read_thread, args=(connection, ))
    read_thread.start()




#boolean to indicate if this peer is acting as the server or not
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_server = False

#get the name and port the user wants to use
name = input("Input user name: ")
self_port = int(input("Enter the port number you want to use: "))

self_address = ("127.0.0.1", self_port)

#create a tcp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(self_address)

response = input("Do you want to host? (Y/N)")

if response == "Y":
    listen_thread = threading.Thread(target=listen_thread, args=(sock, ))
    listen_thread.start()
    listen_thread.join()
    is_server = True
elif response == "N":
    #ask the user which port they want to connect to to chat with
    peer_port = int(input("Which Port Do You Want To Chat With? "))
    peer_address = ("127.0.0.1", peer_port)
    connect(sock, peer_address)
else:
    print ("invalid input")



#constantly let the user send messages to the other peer. Send logic also differs from client and server, so need to use the is_server boolean here too
while True:
    message = input()
    if is_server != False:
        connection.sendall(message.encode())
    else:
        sock.sendall(message.encode())





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


