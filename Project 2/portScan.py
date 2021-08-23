import socket
import sys
from datetime import datetime

#Defining constants
permittedProtocols = ["tcp","udp"]
permittedMachines = ["cse01","cse02","cse03","cse04","cse05","cse06"]

#Checking the input edge cases
if len(sys.argv) < 4 :
    print("Usage: <portScan> <hostname> <protocol> <port low> <port high>")
    sys.exit()
machine = sys.argv[1]
if(machine not in permittedMachines):
    print("Host {} doesn't exist".format(machine))
    sys.exit()
#Assigning Port number
target = socket.gethostbyname(machine)
protocol = sys.argv[2]
low = int(sys.argv[3])
high = int(sys.argv[4])

if(protocol not in permittedProtocols):
    print("Protocol must be TCP or UDP")
    sys.exit()
print("scanning host={},protocol {}, ports: {} -> {}".format(machine,protocol,low,high))

"""
------------------------------------------
If protocol is TCP then
    It will execute the first if condition
else if
    It will go to UDP part of the program
------------------------------------------
"""

if(protocol == 'tcp'):
    try:
        # will scan ports between low to high
        for port in range(low,high):
            #creating TCP connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((target,port))
            if result ==0:
                try:
                    serviceName = socket.getservbyport(port, protocol)
                    print("Port {} is open : {}".format(port,serviceName))
                except:
                    print("Port {} is open : svc name unavail".format(port))
            #closing the open ports
            s.close()
    except KeyboardInterrupt:
            print("\n Exiting Program !!!!")
            sys.exit()
    except socket.gaierror:
            print("\n Hostname Could Not Be Resolved !!!!")
            sys.exit()
    except socket.error:
            print("\ Server not responding !!!!")
            sys.exit()
elif(protocol == 'udp'):
        for port in range(low,high):
            #creating UDP connecction
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msgFromClient = "MESSAGE"
            #setting timeout
            s.settimeout(1)
            try:
                s.connect_ex((target,port))
                s.sendto(msgFromClient.encode(),(target,port))
                msgFromServer = s.recvfrom(2048)
                if(msgFromServer):
                    try:
                        serviceName = socket.getservbyport(port,protocol)
                        print("Port {} is open name: {}".format(str(port),serviceName))
                    except:
                        print("Port {} is open name: svc name unavail".format(port))
            except socket.timeout:
                try:
                    serviceName = socket.getservbyport(port,protocol)
                    print("Port {} is open name: {}".format(str(port),serviceName))
                except:
                     pass
            except:
                try:
                    serviceName = socket.getservbyport(port,protocol)
                    print("Port {} is closed name: {}".format(str(port),serviceName))
                except:
                     pass

