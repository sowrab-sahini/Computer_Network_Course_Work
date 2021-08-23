# Python program to implement server side of chat room.
import socket
import select
import sys
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 2:
    print("Correct usage: script, port number")
    exit()

Port = int(sys.argv[1])
server.bind(('', Port))
server.listen(100)
list_of_clients = []
users = []
fd = []
def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!")
    while True:
        try:
            message = conn.recv(2048)
            if message:
                msg_split = message.split()
                if msg_split[0] == "JOIN":
                    if(len(users) >10):
                        conn.send("Too many users...")
                    elif (msg_split[1] in users):
                        match = users.index(msg_split[1])
                        conn.send("User Already Registered: Username("+msg_split[1]+"), FD(" +str(list_of_clients[match].fileno()))
                    else:
                        users.append(str(msg_split[1]))
                        print(users)
                        conn.send(msg_split[0] + " " + msg_split[1] + " Request Accepted \n")
                elif msg_split[0] == "LIST":
                    if(len(users) == 0):
                        conn.send("Unregistered User. Use JOIN <username> to Register")
                    else:
                        for i in range(0,len(list_of_clients)):
                            print(list_of_clients[i])
                            fd.append(list_of_clients[i].fileno())
                        print(fd)    
                        conn.send("USERNAME"+"\t"+"FD")
                        conn.send("\n--------------\n")
                        for i in range(0,len(fd)):
                            conn.send(users[i]+"\t" + str(fd[i])+"\n")
                        conn.send("--------------\n")
                elif msg_split[0] == "MESG":
                    try:
                        receiver = users.index(msg_split[1])
                        sender = list_of_clients.index(conn)
                        print(msg_split[2:])
                        message = ""
                        for msg in  msg_split[2:len(msg_split)]:
                            message = message + " " + msg
                        if receiver >= 0 and sender >= 0:
                            list_of_clients[receiver].send("\nFrom "+ users[sender] + " : " + message +"\n")
                        else :
                            conn.send("Unknown Recipient(" + msg_split[1]+"). MESG Discarded.")
                    except:
                        print("Error in MESG functionality")
                elif msg_split[0] == "BCST":
                    if len(users) == 0:
                        conn.send("Unregistered User. Use JOIN <username> to register")
                    else:
                        broadcast(msg_split[1],conn)
                elif msg_split[0] == "QUIT":
                    if(len(users) == 0):
                        conn.send("There are no users to remove")
                    remove(conn)
            else:
                """message may have no content if the connection 
                is broken, in this case we remove the connection"""
                remove(conn)
        except:
            continue


"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                sender = list_of_clients.index(connection)
                if sender >= 0:
                    clients.send("From "+ users[sender]+":"+ message)
            except:
                clients.close()
                # if the link is broken, we remove the client
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        rem_id = list_of_clients.index(connection)
        users.pop(rem_id)
        list_of_clients.remove(connection)
        connection.send("Connection closed by foreign host")

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
