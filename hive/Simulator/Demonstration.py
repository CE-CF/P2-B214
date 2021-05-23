# Run the simulation then run this program to demonstrate multiple Tello drones moving

import threading, socket, time

class Parent(threading.Thread):

    def __init__(self, Sock: socket.socket, IP: str):
        super().__init__()
        self.Dest = IP
        self.Sock = Sock
        self.Running = True
        self.Server = ("127.0.0.1", 8889)

    def run(self) -> None:
        pass

    def Stop(self):
        self.Running = False


class CWCircle(Parent):

    def __init__(self, Sock: socket.socket, IP: str):
        super().__init__(Sock, IP)

    def run(self) -> None:
        Command = self.Dest + ": takeoff"
        self.Sock.sendto(bytes(Command, "utf-8"), self.Server)
        Command = self.Dest + ": rc 0 100 0 33"
        while self.Running:
            self.Sock.sendto(bytes(Command, "utf-8"), self.Server)
            time.sleep(1)
        Command = self.Dest + ": stop"
        self.Sock.sendto(bytes(Command, "utf-8"), self.Server)

class CCWCircle(Parent):

    def __init__(self, Sock: socket.socket, IP: str):
        super().__init__(Sock, IP)

    def run(self) -> None:
        Command = self.Dest + ": takeoff"
        self.Sock.sendto(bytes(Command, "utf-8"), self.Server)
        Command = self.Dest + ": rc 0 -100 0 33"
        while self.Running:
            self.Sock.sendto(bytes(Command, "utf-8"), self.Server)
            time.sleep(1)
        Command = self.Dest + ": stop"
        self.Sock.sendto(bytes(Command, "utf-8"), self.Server)

def main():
    Drone_Number = 10
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Threads = []
    for i in range(Drone_Number):
        if (i%2) == 0:
            Thread = CWCircle(Socket, f'0.0.0.{i}')
            Threads.append(Thread)
            Thread.start()
        else:
            Thread = CCWCircle(Socket, f'0.0.0.{i}')
            Threads.append(Thread)
            Thread.start()
    input("Type anything to end program ")
    for i in range(Drone_Number):
        Threads[i].Stop()
        Threads[i].join()
    Socket.close()


main()
