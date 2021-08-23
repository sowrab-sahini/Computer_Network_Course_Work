import socket
import sys
try: 
    if len(sys.argv) == 1 or len(sys.argv)> 2 :
        print("Usage: <filename> <port number>")
        sys.exit()
    localIP = ""
    localPort = int(sys.argv[1])
    bufferSize = 1024
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("Ready to accept data")
    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        print(message)
        if message == "Packet Dropped":
            msgFromServer = "Timed Out"
            packetLost = str.encode(msgFromServer)
            UDPServerSocket.sendto(packetLost, address)
        else:
            # Sending a reply to client
            msgFromServer = "PONG"
            bytesToSend = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)
except KeyboardInterrupt:
        print 'You pressed CTRL + C Server Interrupt '
        sys.exit(0)            
