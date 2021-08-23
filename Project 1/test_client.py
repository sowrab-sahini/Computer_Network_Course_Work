import socket
import time
import sys
import random

skip_packet = []
for i in range(0,3):
    x = random.randint(0,9)
    skip_packet.append(x)
print(skip_packet)    
if len(sys.argv) == 1:
    print("Input Format: <file name> <server name> <port number>")
    sys.exit()      
if len(sys.argv) > 3:
    print("Argumets exceeding Input Format: <filename> <server name> <port number>")
    sys.exit()
localIP = socket.gethostbyname(sys.argv[1])
portNumber = sys.argv[2]
serverAddressPort = (localIP,int(portNumber))
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Send to server using created UDP socket
rtts = []
for i in range(10):
    print(i+1)
    if i in skip_packet:
        sendDropMessage = str.encode("Packet Dropped")
        UDPClientSocket.sendto(sendDropMessage, serverAddressPort)
    else:
        t1 = time.time()
        msgFromClient= "PING"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    if (msgFromServer[0] == "Timed Out"):
        print("Sent..." + msgFromServer[0])
    else:    
       t2=time.time()
       rtt = str(t2-t1) 
       rtts.append(rtt)
       msg = "Sent..."+ msgFromServer[0] + " " + "RTT=" + rtt
       print(msg)
print("-------------------------")
print("Minimun RTT :"+ min(rtts)+" ms")
print("Maximum RTT :"+ max(rtts)+" ms")
number_list = []
for i in rtts:
    rounded = round(float(i),5)
    number_list.append((rounded))
average = sum(number_list)/len(number_list)
unique = []
for i in skip_packet:
        # check if exists in unique_list or not
        if i not in unique:
            unique.append(i)
print("Average RTT :" + str(average)+" ms")
packets_received = 10 - len(unique)
print("10 packets submitted, Packets Received " + str(packets_received)+", "+ str((len(unique)*10)) + "% packet loss")
print("-------------------------")
