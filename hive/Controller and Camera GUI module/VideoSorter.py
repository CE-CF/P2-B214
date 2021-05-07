import threading
import socket
import os
import traceback

"""
This class is used to intercept the video from the 11111 port and then sorts them
It then sends the videos to local ports 22000-22255 depending on the ip of the drone it came from
"""
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

    # This function sorts the data and sends it to the correct local port
    def Send_The_Ting(self,r,a):
        try:
            #print(f'Address received from is: {a}')
            SplitIP = str(a[0]).split('.')
            #print(f'Split IP: {SplitIP}')
            LastIP = SplitIP[-1]
            #print(f'LastIP: {LastIP}')
            while len(LastIP) < 3:
                LastIP = '0' + LastIP
            SendPort = int("22" + LastIP)
            #print(f'Send Port: {SendPort}')
            #FileName = str(a[0]) + '.txt'
            #print(f"The packet length is: {len(r)}")
            #with open(FileName, "wb+") as f:
            #    f.write(r)
            self.Socket.sendto(r, ('127.0.0.1', SendPort))
            #os.chmod(FileName, 0o777)
            #f = open(FileName, 'wb')
            #f.write(r)
            #f.close()
        except OSError:
            print("OSError Caught")
            traceback.print_exc()
            return

    # Run function receives the video frames and then starts a thread for each function that sends the frames
    def run(self):
        TimeoutCount = 0
        while self.Running:
            try:
                r, a = self.Socket.recvfrom(self.BuffSize)
                Send_Thread = threading.Thread(target=self.Send_The_Ting, args=(r,a,))
                Send_Thread.start()
                #print(f'Address received from is: {a}')
                #SplitIP = str(a[0]).split('.')
                #print(f'Split IP: {SplitIP}')
                #LastIP = SplitIP[-1]
                #print(f'LastIP: {LastIP}')
                #while len(LastIP) < 3:
                #    LastIP = '0' + LastIP
                #SendPort = int("22" + LastIP)
                #print(f'Send Port: {SendPort}')
                #FileName = str(a[0]) + '.txt'
                #print(f"The packet length is: {len(r)}")
                #with open(FileName, "wb+") as f:
                #    f.write(r)
                #self.Socket.sendto(r, ('127.0.0.1', SendPort))
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

    # Ends the run thread
    def Finish(self):
        self.Running = False
