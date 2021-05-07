import threading
import socket
import os
import traceback


class VideoSorter(threading.Thread):

    def __init__(self, IP='0.0.0.0', Port=11111, BuffSize=2048):
        super().__init__()
        self.IP = IP
        self.Port = Port
        self.BuffSize = BuffSize
        self.Running = True
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Socket.bind((self.IP,self.Port))
        self.Socket.settimeout(1)

    def run(self):
        TimeoutCount = 0
        while self.Running:
            try:
                r, a = self.Socket.recvfrom(self.BuffSize)
                #print(f'Address received from is: {a}')
                SplitIP = str(a[0]).split('.')
                #print(f'Split IP: {SplitIP}')
                LastIP = SplitIP[-1]
                #print(f'LastIP: {LastIP}')
                while len(LastIP) < 3:
                    LastIP = '0' + LastIP
                SendPort = int("22" + LastIP)
                #print(f'Send Port: {SendPort}')
                FileName = str(a[0]) + '.txt'
                #print(f"The packet length is: {len(r)}")
                #with open(FileName, "wb+") as f:
                #    f.write(r)
                self.Socket.sendto(r, ('127.0.0.1', SendPort))
                #os.chmod(FileName, 0o777)
                #f = open(FileName, 'wb')
                #f.write(r)
                #f.close()
                TimeoutCount = 0
            except socket.timeout:
                TimeoutCount += 1
                print(f'Socket timed out')
            except ConnectionResetError:
                #traceback.print_exc()
                #print("Connection reset error")
                continue
            except:
                print("Some other error occured")
        self.Socket.close()

    def Finish(self):
        self.Running = False
