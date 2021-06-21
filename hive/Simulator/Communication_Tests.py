from socket import *
from threading import Thread

"""Run this script to work as client and send messages to the simulation"""

Run_Receive = True

Server_IP = "127.0.0.1"
#Server_IP = "192.168.137.1"
#SERVER_IP = "192.168.56.1"
Server_Port = 8889
#Bind_Port = 9999
Buffer_Size = 1024

s = socket(AF_INET,SOCK_DGRAM)
s.settimeout(5)
#s.bind((Server_IP, Bind_Port))

def Recieve():
    #global Run_Receive
    print("Receive running")
    #print(f's is: {s}')
    #s.sendto(b'',(Server_IP,Server_Port))
    while Run_Receive:
        Data = s.recvfrom(Buffer_Size)
        if Data == b'':
            continue
        print(f'Data recieved is: {Data}')
    print("Receive stopped")

while True:
    #Receive_Thread = Thread(target=Recieve, name="Receive_Thread")
    #Receive_Thread.start()
    Input_String = input("Enter command: ")
    if Input_String.lower() == "stop":
        #global Run_Receive
        Run_Receive = False
        break
    s.sendto(bytes(Input_String,'utf-8'),(Server_IP,Server_Port))
    print("Data sent.")
    try:
        Data = s.recv(Buffer_Size)
        print(f'Data recieved is: {Data}')
    except timeout:
        print(f'Response timed out')
        print(f'It is highly advised to just restart the client')
    #UTFData = str(Data, encoding="UTF-8")
    #print(f'Data recieved is: {UTFData}')

