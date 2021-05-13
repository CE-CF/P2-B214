import ipaddress
import os
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

class DroneChecker():
    def __init__(self, host):
        self.host = host
        self.host_ip = self.host.split('.')
        self.ip_range = 252
        
    
    def ping(self):
        alive = []
        print('Pinging all hosts on {}.2-254'.format(self.host))
        
        with open(os.devnull, "wb") as limbo:
            for n in range(2, 254):
                    ip="{0}.{1}".format(self.host, n)
                    result=subprocess.Popen(["ping", "-n", "1", "-w", "100", ip],
                            stdout=limbo, stderr=limbo).wait()
                    if result:
                            print(ip + " inactive")
                    else:
                            print(ip + " active")
                            alive.append(ip)
        print("\n")

        return alive
            
            

    def activeDrones(self):
        counter = 0
        active_drone = [[None for x in range(self.ip_range)] for x in range(3)]
        for x in range (2,255):
            new_host_ip = '{}.{}.{}.{}'.format(self.host_ip[0],self.host_ip[1],self.host_ip[2],x)
            if self.ping(new_host_ip):
                print('The drone at IP: {} is online'.format(new_host_ip))
                active_drone[counter][0] = 'RelayBox1_Drone{}'.format(counter)
                active_drone[counter][1] = new_host_ip
                active_drone[counter][2] = "Online"
            else:
                print('The drone at IP: {} is offline'.format(new_host_ip))
        
        return active_drone